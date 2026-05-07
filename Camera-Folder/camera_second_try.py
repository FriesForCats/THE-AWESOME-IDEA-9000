import cv2
import torch
import mysql.connector
import sys
import warnings
import time
from camera_setup import caps

# SETUP & SUPPRESS WARNINGS
warnings.filterwarnings("ignore", category=FutureWarning)
last_logged_time = {} 
LOG_COOLDOWN = 10

# DATABASE CONNECTION 
try:
    db = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="password", # very secure password
        database="vision_project",
        port=3306
    )
    cursor = db.cursor()
    print("Successfully connected to the database!")
    
except mysql.connector.Error as err:
    print(f"Database Connection Error: {err}")
    sys.exit()
    
# LOAD MODEL
device = 'cuda' if torch.cuda.is_available() else 'cpu' # Using 'cuda' if you have an NVIDIA GPU, otherwise 'cpu'
model = torch.hub.load('ultralytics/yolov5', 'custom', path='Camera-Folder/detection.pt', device=device) # V5 yolo model 
model.classes = [0, 24,39,41,46,47,49,54,55] # [person,  backpack, bottle, cup, banana, apple, orange, donut, cake]
model.conf = 0.6 # confidence
model.iou = 0.3 # intersection over union

color_map = {
    0  :  (255, 0, 0),     # Person:   Blue (stands out vs everything)
  
    24 :  (255, 255, 255), # Backpack: Black
    39 :  (255, 255, 0),   # Bottle:   Cyan
    41 :  (0, 0, 0),       # Cup:      White
    46 :  (0, 255, 255),   # Banana:   Yellow
    47 :  (0, 0, 255),     # Apple:    Red
    49 :  (0, 165, 255),   # Orange:   Orange
    54 :  (19, 69, 139),   # Donut:    Brown 
    55 :  (203, 192, 255), # Cake:     Pink
}




def videoPlay():
    """ main function for video capturing and item detection. 
    Args:
        None
        
    Returns:
        None
    """
    
    
    i = 0               # variables used for
    curcap = caps[i]    # keeping track of current camera
    cap_width = 800
    use_cameras = True
    held_items = [] # placeholder to allow held items to be passed in at beginning
    
    while use_cameras == True:
        ret, frame = curcap.read()     # Is camera running, numpy array 
        if not ret:
            print("Error: Failed to capture image.")
            break
        
        img = frame.copy() # drawing on copied frame is less intensive than no copy
    
        detections = detect(model, frame)
        
        held_items, returned = check_pairs(detections, model, held_items)
        
        img = draw(img, detections, model, color_map, held_items)
        
        log_items(held_items, returned, cursor, db, last_logged_time, LOG_COOLDOWN)
        
            
        img = resize(img, cap_width)
        
        cv2.imshow("feed", img)
        
        key = cv2.waitKey(1) & 0xFF # millisec of delay before getting input in integer value
        use_cameras, curcap, cap_width, i = get_inputs(key, use_cameras, cap_width, curcap, caps, i)

    curcap.release()
    cv2.destroyAllWindows()
        


# Many arguments displayed as "any" or "object" as actual types cause errors

def detect(model: object, frame):
    """Detects items in a given frame
    
    Args:
        model: The yolov5 model used to detect
        
        frame: A numpy array storing the height, width and BGR color channels

    Returns:
        detections: A list storing the x1, y1, x2, y2, conf, and cls values of the detections
    """
    
    
    results = model(frame, size=256) # lower size for faster speed
    detections = results.xyxy[0].cpu().numpy() 
    return detections


def draw(img, detections, model: object, colors: dict, held_items: list):
    """Draws on the image to display boxes around items, the name of the item and the model's confidence along with the user's cart
    
    Args:
        img: the copied frame to be drawn on
    
        detections: a list storing the x1, y1, x2, y2, conf, and cls values of the detections
        
        model: the yolov5 model used to detect
        
        colors: a dictionary of the class values items have along wtih the BGR list for their associated color
        
        held_items: a list of the items in a users cart
    
    Returns:
        img: the updated image displaying details and boxes around items along with the user's cart
        """
        
    
    for det in detections:
        x1, y1, x2, y2, conf, cls = det
        label = f"{model.names[int(cls)]} {conf:.2f}" # class of item detected and confidence
        color = color_map[cls] # color given by color map of item detected
        
        cv2.rectangle(img, (int(x1), int(y1)), (int(x2), 
                    int(y2)), color, 2) # draws box
        cv2.putText(img, label, (int(x1), int(y1) - 10), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2) # draws label
        
    item_names = [] # names of items in user's cart
    for held in held_items:
        item_names.append(held[0]) 
        
    cv2.putText(img, f"Cart: {item_names}", (20, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3) # draws cart
    
    return img


def check_pairs(detections, model: object, prev_held: list):
    """Checks for item midpoints enclosed in a person's box and items no longer enclosed in aa person's box
    
    Args:
        detections: a list storing the x1, y1, x2, y2, conf, and cls values of the detections

        model: the yolov5 model used to detect
        
        prev_held: the items held in the previous frame
        
    Returns:
        held_items: the list of items whose midpoints are enclosed in the person's box
        
        returned: the held_items list from last frame minus the items still enclosed in the person's box
    """
    
    
    held_items = []
    returned = []
    
    persons = [d for d in detections if model.names[int(d[5])] == "person"]
    items   = [d for d in detections if model.names[int(d[5])] != "person"]

    # checks for items midpoints in person box
    for person in persons:
        for item in items:
            px1, py1, px2, py2 = person[:4] # only x and y values of person list
            ix1, iy1, ix2, iy2 = item[:4]   # only x and y values of item list

            cx = (ix1 + ix2) / 2    # the midpoint of the items x values
            cy = (iy1 + iy2) / 2    # the midpoint of the items y values
            is_inside = px1 <= cx <= px2 and py1 <= cy <= py2 # checks if midpoint is in person box
            if is_inside:
                item_name = model.names[int(item[5])] 
                held_items.append((item_name, item))
    
    # checks for items no longer in person box
    for item_name, item in prev_held:
        if item_name not in held_items:
            returned.append((item_name, item,))

    return held_items, returned


def log_items(held_items, returned, cursor, db, last_logged_time: dict, LOG_COOLDOWN: int):
    """Updates the current inventory in the database while also adding and subtracting from user's cart
    
    Args:
        held_items: the list of items whose midpoints are enclosed in the person's box
        
        returned: the held_items list from last frame minus the items still enclosed in the person's box
        
        cursor: Used to execute code into sql database    see db.cursor()  (~line 23)
        
        db: The database user carts are stored in along with the held inventory
        
        last_logged_time: The last time the database was updated with a certain object
        
        LOG_COOLDOWN: a cooldown between database logs to not constantly update the database with the same object
        
    Returns:
        None
        
    INVENTORY TABLE 
    +----+-------------------------+--------+--------+
    | id | timestamp               | label  | amount |
    +----+-------------------------+--------+--------+
    |  1 | YEAR-MONTH-DAY Hr:Mn:Sc | item 1 |    int |
    |  2 | YEAR-MONTH-DAY Hr:Mn:Sc | item 2 |    int |
    |  3 | YEAR-MONTH-DAY Hr:Mn:Sc | item 3 |    int |
    +----+-------------------------+--------+--------+
    and so on...
    
    DETECTION LOGS TABLE (CART)
    
    """
        
        
    current_time = time.time()

    # loops through each held item, logging it out of inventory and into user cart
    for item_name, item in held_items:
        # print(f"Cart: {item_name}")
        
        
        if item_name not in last_logged_time or (current_time - last_logged_time[item_name] > LOG_COOLDOWN): # checks if item has been recently logged
            

            try:
                cursor.execute("SELECT amount FROM inventory WHERE label = %s", (item_name,)) # item name put as %s
                exists = cursor.fetchone() # checks if the selected row exists
                
                if exists:
                    sql1 = "INSERT INTO detection_logs (label, confidence, status) VALUES (%s, %s, %s)" # adds a row to detection_logs (%s, %s, %s) values are used in the the cells for label, confidence, and status
                    cursor.execute(sql1, (item_name, float(item[4]), "HELD")) # values for (%s, %s, %s)
                    
                    
                    sql2 = "UPDATE inventory SET amount = amount - %s WHERE label = %s" 
                    cursor.execute(sql2, (1,item_name)) # amount - 1  WHERE label = item_name
                    
                    db.commit() # updates database with cursor executions
                

                last_logged_time[item_name] = current_time # sets last_logged_time for item
                print(f"New {item_name} added to cart!")
                
                
            except mysql.connector.Error as e:
                print(f"Logging error: {e}")
    
    for item_name, item in returned:
        
        try: 
            cursor.execute("SELECT amount FROM inventory WHERE label = %s", (item_name,))
            exists = cursor.fetchone()
            
            if exists:
                sql1 = "DELETE FROM detection_logs WHERE label = %s LIMIT 1" # deletes a line from detection_logs when item taken from cart
                cursor.execute(sql1, (item_name,))
                
                sql2 = "UPDATE inventory SET amount = amount + %s WHERE label = %s" # adds 1 to the amount of the item put back on shelf
                cursor.execute(sql2, (1, item_name))
                
                db.commit()
                
                    
        except mysql.connector.Error as e:
            print(f"Logging error: {e}")
                
                

def get_inputs(key: int, use_cameras: bool, cap_width: int, curcap: int, caps: list, i: int):
    """ Uses key value to detect user input during the frame to close the program, switch camera, or increase/decrease screen size
    
    Args:
        key: an integer value expressing the key pressed by a user
        
        use_cameras: a boolean value which when made false ends the video feed and detection
        
        cap_width: width of video feed, used to keep aspect ratio the same when size changes
        
        curcap: the current camera used
        
        caps: the list of captures
        
        i: integer used to traverse caps
    
    Returns:
        use_cameras: a boolean value which when made false ends the video feed and detection
        
        curcap: the current camera used
        
        cap_width: width of the new feed, used to keep aspect ratio the same when size changes

        i: integer used to traverse caps        
    """
    
    # Quits recording
    if key == ord('q') or cv2.getWindowProperty("feed", cv2.WND_PROP_VISIBLE) < 1:
        use_cameras = False
        
    # Switches camera
    elif key == ord(' '):
        i += 1
        if i == len(caps):
            i = 0
        curcap = caps[i]
        time.sleep(0.5)
        
    # Increase or decrease screen size
    elif key == ord('=') or key == ord('+'):
        cap_width += 50
        
    elif key == ord('-') or key == ord('_'):
        cap_width -= 50
    
    # checks if cap_width is too small
    cap_width = max(100, cap_width)
        
    return use_cameras, curcap, cap_width, i


def resize(img, cap_width):
    """ Resizes capture while keeping the same aspect ratio
    
    Args: 
        img: the copied frame to have its size changed
        
        cap_width: The capture's width after changing size
        
    Returns:
        img: the copied frame with its size changed
    
    """
    
    h, w = img.shape[:2] # the height and width of the img array
    ratio = cap_width / float(w) # calculates aspect ratio
    img = cv2.resize(img, (cap_width, int(h * ratio)))
    
    return img