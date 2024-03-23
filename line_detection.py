import imutils
import numpy as np
import cv2
import requests
import time

url = "http://192.168.1.102:8080/shot.jpg"


t2 = time.time()

while(True):

    img_resp = requests.get(url) 
    img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8) 
    captured_frame = cv2.imdecode(img_arr, -1) 
    captured_frame = imutils.resize(captured_frame, width=1000, height=1800)
    
    output_frame = captured_frame.copy()

    captured_frame_bgr = cv2.cvtColor(captured_frame, cv2.COLOR_BGRA2BGR)

    captured_frame_bgr = cv2.medianBlur(captured_frame_bgr, 3)
    captured_frame_lab = cv2.cvtColor(captured_frame_bgr, cv2.COLOR_BGR2Lab)
    # Threshold the Lab image, keep only the red pixels
    # Possible yellow threshold: [20, 110, 170][255, 140, 215]
    # Possible blue threshold: [20, 115, 70][255, 145, 120]
    captured_frame_lab_red = cv2.inRange(captured_frame_lab, np.array([20, 150, 150]), np.array([190, 255, 255]))
    # Second blur to reduce more noise, easier line detection
    captured_frame_lab_red = cv2.GaussianBlur(captured_frame_lab_red, (5, 5), 2, 2)
    # Use the Hough transform to detect lines in the image
    edges = cv2.Canny(captured_frame_lab_red, 50, 150, apertureSize=3)
    lines = cv2.HoughLinesP(
            edges, # Input edge image
            1, # Distance resolution in pixels
            np.pi/180, # Angle resolution in radians
            threshold=100, # Min number of votes for valid line
            minLineLength=5, # Min allowed length of line
            maxLineGap=10 # Max allowed gap between line for joining them
            )
    try:
        for points in lines:
        # Extracted points nested in the list
            x1,y1,x2,y2=points[0]
            # Draw the lines joing the points
            # On the original image
            cv2.line(output_frame,(x1,y1),(x2,y2),(255,255,0),2)
            print('line detected')
            t1 = time.time()
            print(t1-t2)

    except:
        print('Error no line detected')
        t1 = time.time()
        print(t1-t2)

    cv2.imshow('test',output_frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()


