import numpy as np
import cv2

camera =cv2.VideoCapture(0)

while True:
    success, frame = camera.read()
    if not success:
        print("Failed to capture frame")
        break
    
    frame = cv2.flip(frame, 1)
    gray  = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 150, 300)
    
    contours, hierarchy = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    output = frame.copy()
    output2 = frame.copy()
    cv2.drawContours(output, contours, -1, (0, 255, 0), 2)
    
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 80: 
            x, y, w, h = cv2.boundingRect(contour)
            
            cv2.rectangle(output2, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.putText(output2,
                f"Area: {int(area)}",(x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,0.5,
                (0, 0, 255),1)

    #cv2.imshow('My webcam', frame)
    cv2.imshow('Grayscale', gray)
    cv2.imshow("Edges", edges)
    cv2.imshow("Contours", output)
    cv2.imshow("Filtered Contours", output2)
    
    #print(len(contours))

    if cv2.waitKey(1) == ord('q'):
        break
    
camera.release()
cv2.destroyAllWindows()
