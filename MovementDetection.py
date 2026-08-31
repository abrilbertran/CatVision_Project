import cv2

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    raise SystemExit

prev_frame = None
trajectory = []
frame_count = 0

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture frame")
        break

    frame = cv2.flip(frame, 1)
    gray  = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    if prev_frame is not None:
        diff = cv2.absdiff(prev_frame, gray)
        
        # 1. detect motion
        _, thresh = cv2.threshold(diff, 40, 255, cv2.THRESH_BINARY) 
        kernel    = None
        thresh    = cv2.dilate(thresh, kernel, iterations=5)
        #thresh    = cv2.erode(thresh, kernel, iterations=1)
        
        # 2. find contours of the motion
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # 3. draw bounding boxes of largest contours
        if contours:
            largest_contour = max(contours, key=cv2.contourArea)
            area = cv2.contourArea(largest_contour)
            
            if area > 1500: 
                
                # Bounding box
                x, y, w, h = cv2.boundingRect(largest_contour)
                center_x = x + w // 2
                center_y = y + h // 2
                
                # Trajectory tracking
                frame_count += 1
                if frame_count % 7 == 0: 
                    trajectory.append((center_x, center_y))
                    
                #print(center_x, center_y)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                cv2.circle(frame, (center_x, center_y), 5, (0, 255, 0), -1)
                
                for point in trajectory:
                    cv2.circle(frame, point, 5, (255, 0, 0), -1)
           
        cv2.imshow("Threshold", thresh)
        cv2.imshow("Movement Detection", frame)
    else:
        cv2.imshow("Movement Detection", gray)
        

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    prev_frame = gray

cap.release()
cv2.destroyAllWindows()
