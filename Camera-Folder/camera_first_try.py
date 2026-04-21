import cv2
from time import sleep
# from matplotlib import pyplot as plt
# import numpy as np
# from ultralytics import YOLO
import torch
import math 
model = torch.hub.load('ultralytics/yolov5', 'custom', path='Camera-Folder/detection.pt')

model.conf = 0.4  # Set confidence threshold to 60%
model.IOU = 0.45  # 

cap  = cv2.VideoCapture(0) 
cap2 = cv2.VideoCapture(1)

# checks to see if captures work
has_cap = cap.isOpened()
has_cap2 = cap2.isOpened()

def videoPlay():
    
    curcap = cap if has_cap else cap2 # checks to see if more than one video feed exists
    prev_key = 'None' # Defaults the previous key stroke to None
    cap_width = 800 # Default width of video feed
    
    while True:
        
            
        
        #getting a frame from the camera
        ret, frame = curcap.read()
        

        #makes sure the camera can be read
        if not ret:
            print("Error: Failed to capture image.")
            break
        
        #gets the height and width of the camera feed for later
        h, w = frame.shape[:2]
        
        
        # # Pre-process: create a 300x300 blob 
        # blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0,(300, 300), (104.0, 177.0, 123.0))
        # "This line ^ shrinks the image into a 300 x 300 square "
        # "and then scales it to stay 300 x 300p "
        # "and finally takes all the color out"
    
        # # Run detection
        # net.setInput(blob)
        # detections = net.forward()

        # # Loop over detections
        # for i in range(0, detections.shape[2]):
        #     confidence = detections[0, 0, i, 2]

        #     # Filter out weak detections (< 50% confidence)
        #     if confidence > 0.5:
        #         # Scale coordinates back to original frame size 
        #         box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
        #         (startX, startY, endX, endY) = box.astype("int")


        #         # Converts the confidence of the face into a percent
        #         text = f"{confidence * 100:.2f}%"
                
        #         # Box drawing
        #         cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 255, 0), 2)
        #         # Percent Drawing
        #         cv2.putText(frame, text, (startX, startY - 10),
        #                     cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 0), 2)
        
        
        results = model(frame, size=416) # shrinks image for ai to 
        
        img = frame.copy()
        
        # manually draws box for better control and speed
        for *box, conf, cls in results.xyxy[0]: # 
            x1, y1, x2, y2 = map(int, box) # cords of box corners
            label = f"{model.names[int(cls)]} {conf:.2f}" # draws label with class and confidence
            
            # gives different but distinct colors to the boxes and labels 
            color = (
                int((cls * 37) % 255), 
                int((cls * 17) % 255),
                int((cls * 29) % 255)
            )           
            # Get detections as a numpy array
        detections = results.xyxy[0].cpu().numpy()
        
        for i in range(len(detections)):
            for j in range(i + 1, len(detections)):
                # Data for first object
                x1_a, y1_a, x2_a, y2_a, conf_a, cls_a = detections[i]
                name_a = model.names[int(cls_a)]
                
                # Data for second object
                x1_b, y1_b, x2_b, y2_b, conf_b, cls_b = detections[j]
                name_b = model.names[int(cls_b)]

                # Initialize variables to identify who is the person and who is the item
                person_box = None
                item_box = None

                # Check if one is a person and the other is NOT a person
                if name_a == "person" and name_b != "person":
                    person_box = (x1_a, y1_a, x2_a, y2_a)
                    item_box = (x1_b, y1_b, x2_b, y2_b)
                    item_name = name_b
                elif name_b == "person" and name_a != "person":
                    person_box = (x1_b, y1_b, x2_b, y2_b)
                    item_box = (x1_a, y1_a, x2_a, y2_a)
                    item_name = name_a

                # If we found a Person + Item pair, check for containment
                if person_box and item_box:
                    px1, py1, px2, py2 = person_box
                    ix1, iy1, ix2, iy2 = item_box

                    # STRICT LOGIC: All edges of the item must be inside the person's edges
                    is_inside = (ix1 >= px1 and iy1 >= py1 and 
                                 ix2 <= px2 and iy2 <= py2)

                    if is_inside:
                        status = f"HELD/CONTAINED: {item_name.upper()}"
                        color = (0, 255, 0) # Green for "Success/Inside"
                        
                        # Visual notification
                        cv2.rectangle(img, (int(px1), int(py1)), (int(px2), int(py2)), color, 2)
                        cv2.rectangle(img, (int(ix1), int(iy1)), (int(ix2), int(iy2)), color, 4)
                        cv2.putText(img, status, (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 3)
            
            # displays box and label on screen
            cv2.rectangle(img, (x1, y1), (x2, y2), (color), 2)
            cv2.putText(img, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (color), 2)

        frame = img
           
        # Resizes live feed to match a given width, allowing for simillar sizes in the case of two webcams
        h, w = frame.shape[:2]
        ratio = cap_width / float(w)
        cap_height = int(h * ratio)
        shown_frame = cv2.resize(frame, (cap_width, cap_height))
        
        #Shows the image in a live feed
        cv2.imshow("feed",shown_frame)

        key = cv2.waitKey(1) & 0xFF
        
        # Several inputs used to kill camera stream
        if key == ord('q'):
            break
        elif key == ord('\x1b'):
            break
        elif cv2.getWindowProperty("feed", cv2.WND_PROP_VISIBLE) < 1:
            break
        
        # Input to switch video feed
        elif key == ord(' '):
            if prev_key != ' ':
                if curcap == cap:
                    curcap = cap2
                    sleep(0.5)
                else:
                    curcap = cap
                    sleep(0.5)
                prev_key = ' '
                
        # Increase or decrease screen size
        elif key == ord('=') or key == ord('+'):
            cap_width += 50
        elif key == ord('-') or key == ord('_'):
            cap_width -= 50
        
        # bug fix for switching camera
        else:
            prev_key = 'None'

    #Releases camera and windows captured
    curcap.release()
    cv2.destroyAllWindows()


# Only executed when this file is run, used for bug fixing with the video feed              (and for when I accidently run this file instead of main)
if __name__ == "__main__":
    videoPlay()