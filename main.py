import numpy as np
import cv2

camera =cv2.VideoCapture(0)

while True:
    success, frame = camera.read()
    if not success:
        print("Failed to capture frame")
        break
    
    frame = cv2.flip(frame, 1)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150)
    
    cv2.imshow('My webcam', frame)
    cv2.imshow('Grayscale', gray)
    cv2.imshow("Edges", edges)
    

    if cv2.waitKey(1) == ord('q'):
        break
    
camera.release()
cv2.destroyAllWindows()
