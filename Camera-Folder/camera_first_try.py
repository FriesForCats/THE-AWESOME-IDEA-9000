import cv2
from time import sleep
from matplotlib import pyplot as plt
import numpy as np


prototxt_path = "deploy.prototxt"
model_path = "res10_300x300_ssd_iter_140000.caffemodel"

net = cv2.dnn.readNetFromCaffe(prototxt_path, model_path)

cap  = cv2.VideoCapture(0) # Set to 0 for built in webcam if 1 does not work
cap2 = cv2.VideoCapture(1)

has_cap = cap.isOpened()
has_cap2 = cap2.isOpened()

def videoPlay():
    curcap = cap if has_cap else cap2
    prev_key = 'None'
    while True:
        
            
        
        #getting a frame from the camera
        ret, frame = curcap.read()

        #makes sure the camera can be read
        if not ret:
            print("Error: Failed to capture image.")
            break
        
        #gets the height and width of the camera feed for later
        h, w = frame.shape[:2]
        
        # Pre-process: create a 300x300 blob 
        blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0,(300, 300), (104.0, 177.0, 123.0))
        "This line ^ shrinks the image into a 300 x 300 square "
        "and then scales it to stay 300 x 300p "
        "and finally takes all the color out"
    
        # Run detection
        net.setInput(blob)
        detections = net.forward()

        # Loop over detections
        for i in range(0, detections.shape[2]):
            confidence = detections[0, 0, i, 2]

            # Filter out weak detections (< 50% confidence)
            if confidence > 0.5:
                # Scale coordinates back to original frame size 
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")


                # Converts the confidence of the face into a percent
                text = f"{confidence * 100:.2f}%"
                
                # Box drawing
                cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 255, 0), 2)
                # Percent Drawing
                cv2.putText(frame, text, (startX, startY - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 0), 2)
                
        #Shows the image in a life feed
        cv2.imshow("feed",frame)

        #Used to kill camera stream
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        if cv2.waitKey(1) & 0xFF == ord('\x1b'): # ESC key wworks to delete video feed
            break
        if cv2.getWindowProperty("feed", cv2.WND_PROP_VISIBLE) < 1:
            break
        if cv2.waitKey(1) & 0xFF == ord(' '):
            if prev_key != ' ':
                if curcap == cap:
                    curcap = cap2
                    sleep(0.5)
                else:
                    curcap = cap
                    sleep(0.5)
                prev_key = ' '
            
        if cv2.waitKey(1) & 0xFF != ord(' '):
            prev_key = 'None'

    #Releases camera and windows captured
    curcap.release()
    cv2.destroyAllWindows()
