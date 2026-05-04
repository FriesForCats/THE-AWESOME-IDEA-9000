import cv2
import torch
import mysql.connector
import sys
import warnings
import time

# 1. SETUP & SUPPRESS WARNINGS
warnings.filterwarnings("ignore", category=FutureWarning)
last_logged_time = {} 
LOG_COOLDOWN = 10




# 2. DATABASE CONNECTION (Keep this outside the loop for speed!)
try:
    db = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="password", # Update to your actual password
        database="vision_project",
        port=3306
    )
    cursor = db.cursor()
    print("Successfully connected to the database!")
except mysql.connector.Error as err:
    print(f"Database Connection Error: {err}")
    sys.exit()

# 3. LOAD MODEL
# Using 'cuda' if you have an NVIDIA GPU, otherwise 'cpu'
device = 'cuda' if torch.cuda.is_available() else 'cpu'
model = torch.hub.load('ultralytics/yolov5', 'custom', path='detection.pt', device=device)
model.classes = [0,  24, 39, 41, 46, 47, 49, 54, 55] # [person,  backpack, bottle, cup, banana, apple, orange, donut, cake]
model.conf = 0.4 
model.iou = 0.3 # Lowered slightly to help detect overlapping objects

# 3.5 COLOR MAP AND OTHER VARIABLES
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

# 4. CAMERA SETUP
cap = cv2.VideoCapture(0)
cap2 = cv2.VideoCapture(1)
has_cap = cap.isOpened()
has_cap2 = cap2.isOpened()

def videoPlay():
    curcap = cap if has_cap else cap2
    cap_width = 800
    
    while True:
        ret, frame = curcap.read()
        if not ret:
            print("Error: Failed to capture image.")
            break

        # Run detection (size 320 is faster than 416)
        results = model(frame, size=320)
        img = frame.copy()
        detections = results.xyxy[0].cpu().numpy()
        

        # --- STEP A: DRAW ALL OBJECTS FIRST ---
        # This ensures you see everything the AI sees
        for det in detections:
            x1, y1, x2, y2, conf, cls = det
            label = f"{model.names[int(cls)]} {conf:.2f}"
            color = color_map[cls] # Cyan for general detections
            
            cv2.rectangle(img, (int(x1), int(y1)), (int(x2), int(y2)), color, 2)
            cv2.putText(img, label, (int(x1), int(y1) - 10), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

        # --- STEP B: CHECK FOR PAIRS (HELD LOGIC) ---
        for i in range(len(detections)):
            for j in range(i + 1, len(detections)):
                d1, d2 = detections[i], detections[j]
                name1, name2 = model.names[int(d1[5])], model.names[int(d2[5])]

                person = None
                item = None 
                held_items = []

                # Logic to identify Person vs Item
                if name1 == "person" and name2 != "person":
                    person, item = d1, d2
                elif name2 == "person" and name1 != "person":
                    person, item = d2, d1

                if person is not None and item is not None:
                    # Bounding Box Containment Check
                    px1, py1, px2, py2 = person[:4]
                    ix1, iy1, ix2, iy2 = item[:4]

                    is_inside = (ix1 >= px1 and iy1 >= py1 and ix2 <= px2 and iy2 <= py2)

                    if is_inside:
                        held_items.append(model.names[int(item[5])])
                        item_name = model.names[int(item[5])]
                        current_time = time.time()
                        print(f"Cart: {held_items}.")
                        
                        # Visual notification
                        cv2.putText(img, f"HELD: {item_name.upper()}", (20, 50), 
                                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)

                        # LOG TO DATABASE
                        if item_name not in last_logged_time or (current_time - last_logged_time[item_name] > LOG_COOLDOWN):
                            try:
                                sql = "INSERT INTO detection_logs (label, confidence, status) VALUES (%s, %s, %s)"
                                cursor.execute(sql, (item_name, float(item[4]), "HELD"))
                                db.commit()
                                
                                # Update the timestamp
                                last_logged_time[item_name] = current_time
                                print(f"Database Updated: {item_name}")
                            except mysql.connector.Error as e:
                                print(f"Logging error: {e}")
        # Resize and Show
        h, w = img.shape[:2]
        ratio = cap_width / float(w)
        shown_frame = cv2.resize(img, (cap_width, int(h * ratio)))
        
        cv2.imshow("feed", shown_frame)

        # Handle Inputs
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q') or cv2.getWindowProperty("feed", cv2.WND_PROP_VISIBLE) < 1:
            break
        elif key == ord(' '): # Switch Camera
            curcap = cap2 if curcap == cap else cap
            time.sleep(0.5)
        # Increase or decrease screen size
        elif key == ord('=') or key == ord('+'):
            cap_width += 50
        elif key == ord('-') or key == ord('_'):
            cap_width -= 50
    curcap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    videoPlay()