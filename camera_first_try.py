import cv2
from time import sleep
from matplotlib import pyplot as plt

cap =cv2.VideoCapture(1)


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

#releases camera and windows captured
cap.release()
cv2.destroyAllWindows()




