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
    
    i = 0
    curcap = caps[i]
    cap_width = 800
    
    while True:
        ret, frame = curcap.read()
        if not ret:
            print("Error: Failed to capture image.")
            break
        
        img = frame.copy()
    
        detections = detect(model, frame)
        
        img = draw(img, detections, model, color_map)
        
        held_items = check_pairs(detections, model)
        
        log_items(held_items, cursor, db, last_logged_time, LOG_COOLDOWN)
        
        
        h, w = img.shape[:2]
        ratio = cap_width / float(w)
        shown_frame = cv2.resize(img, (cap_width, int(h * ratio)))
        cv2.imshow("feed", shown_frame)
        
        
        key = cv2.waitKey(1) & 0xFF
        
        if key == ord('q') or cv2.getWindowProperty("feed", cv2.WND_PROP_VISIBLE) < 1:
            break
        elif key == ord(' '): # Switch Camera
            i += 1
            if i == len(caps):
                i = 0
            curcap = caps[i]
            time.sleep(0.5)
        # Increase or decrease screen size
        elif key == ord('=') or key == ord('+'):
            cap_width+=50
        elif key == ord('-') or key == ord('_'):
            cap_width-=50
        
        #cv2.imshow("feed", frame)
    curcap.release()
    cv2.destroyAllWindows()
        

def detect(model, frame):
    """detects images yadayada"""
    results = model(frame, size=256) # lower size for faster speed
    detections = results.xyxy[0].cpu().numpy()
    return detections


def draw(img, detections, model, colors):
    """draws images yadayada"""
    for det in detections:
        x1, y1, x2, y2, conf, cls = det
        label = f"{model.names[int(cls)]} {conf:.2f}"
        color = color_map[cls]
        
        cv2.rectangle(img, (int(x1), int(y1)), (int(x2), int(y2)), color, 2)
        cv2.putText(img, label, (int(x1), int(y1) - 10), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
    
    return img


def check_pairs(detections, model):
    """checks pairs yadayada"""
    held_items = []

    for i in range(len(detections)):
        for j in range(i + 1, len(detections)):
            d1, d2 = detections[i], detections[j]
            name1, name2 = model.names[int(d1[5])], model.names[int(d2[5])]

            person, item = None, None

            if name1 == "person" and name2 != "person":
                person, item = d1, d2
            elif name2 == "person" and name1 != "person":
                person, item = d2, d1

            if person is not None and item is not None:
                px1, py1, px2, py2 = person[:4]
                ix1, iy1, ix2, iy2 = item[:4]

                is_inside = (ix1 >= px1 and iy1 >= py1 and ix2 <= px2 and iy2 <= py2)

                if is_inside:
                    item_name = model.names[int(item[5])]
                    held_items.append((item_name, item))

    return held_items


def log_items(held_items, cursor, db, last_logged_time, LOG_COOLDOWN):
    """logs items into database"""
    current_time = time.time()

    for item_name, item in held_items:
        print(f"Cart: {item_name}")

        if item_name not in last_logged_time or (current_time - last_logged_time[item_name] > LOG_COOLDOWN):
            try:
                sql = "INSERT INTO detection_logs (label, confidence, status) VALUES (%s, %s, %s)"
                cursor.execute(sql, (item_name, float(item[4]), "HELD"))
                db.commit()

                last_logged_time[item_name] = current_time
                print(f"Database Updated: {item_name}")
            except mysql.connector.Error as e:
                print(f"Logging error: {e}")


def resize(img, cap_width):
        h, w = img.shape[:2]
        ratio = cap_width / float(w)
        frame = cv2.resize(img, (cap_width, int(h * ratio)))
        
        return frame









    
    