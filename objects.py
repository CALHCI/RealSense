import cv2 as cv
from itertools import zip_longest
import numpy as np

cap = cv.VideoCapture(0)

tracker = cv.TrackerMIL_create()

ret, frame = cap.read()

bbox = cv.selectROI("Frame", frame, fromCenter=False, showCrosshair=True)

tracker.init(frame, bbox)

while True:
    #Read each frame
    ret, frame = cap.read()
    if not ret:
            break
        
    ret, bbox = tracker.update(frame)
    # Draw bounding box around the tracked object
    if ret:
        x, y, w, h = map(int, bbox)
        cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            
    cv.imshow("ROI", frame)

    key = cv.waitKey(30)

    if key == 27:
        break
    
cap.release()
cv.destroyAllWindows()
