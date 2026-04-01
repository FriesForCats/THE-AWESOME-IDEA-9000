import cv2
from time import sleep
from matplotlib import pyplot as plt

cap =cv2.VideoCapture(1) # Set to 0 for built in webcam if 1 does not work


while True:
    #getting a frame from the camera
    ret, frame = cap.read()

    #makes sure the camera can be read
    if not ret:
        print("Error: Failed to capture image.")
        break
    
    #shows frame in a window
    cv2.imshow("feed",frame)

    #used to kill camera stream
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    if cv2.waitKey(1) & 0xFF == ord('\x1b'): # ESC key wworks to delete video feed
        break
    if cv2.getWindowProperty("feed", cv2.WND_PROP_VISIBLE) < 1:
        break

#releases camera and windows captured
cap.release()
cv2.destroyAllWindows()
