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
        
        detect()
        
        display()
        
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
            cap_width += 50
        elif key == ord('-') or key == ord('_'):
            cap_width -= 50
    curcap.release()
    cv2.destroyAllWindows()
        

def detect():
    """detects images yadayada"""
    pass


def draw():
    """draws images yadayada"""
    pass


def check_pairs():
    """checks pairs yadayada"""
    pass


def log():
    """logs database or something"""
    pass


def display():
    """displays the window with detection"""
    pass









    
    