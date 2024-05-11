import imutils
import numpy as np
import cv2
import requests
import matplotlib.pyplot as plt
import playsound 
url = "http://192.168.1.103:8080/shot.jpg"

X_axis ,Y_axis= [],[]

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
    captured_frame_lab_red = cv2.inRange(captured_frame_lab, np.array([30, 150, 150]), np.array([190, 255, 255])) 
    sensitivity = 15
    lower_white = np.array([0,0,255-sensitivity])
    upper_white = np.array([255,sensitivity,255])  
    captured_frame_lab_white = cv2.inRange(captured_frame_lab, lower_white, upper_white) 
    # Second blur to reduce more noise, easier circle detection
    captured_frame_lab_white = cv2.GaussianBlur(captured_frame_lab_red, (5, 5), 2, 2)
    # Use the Hough transform to detect circles in the image
    circles = cv2.HoughCircles(captured_frame_lab_white, cv2.HOUGH_GRADIENT, 1, captured_frame_lab_white.shape[0] / 8, param1=100,
                                param2=18, minRadius=2, maxRadius=20)
    
    
    if circles is None:
        playsound.playsound('nothing_detected.mp3')
        cv2.putText(output_frame,'0 laser detected',(50,50),cv2.FONT_HERSHEY_COMPLEX_SMALL,0.6,255)

    elif circles is not None:
        if len(circles[0]) > 1:
            playsound.playsound('more_than_one.mp3')
            cv2.putText(output_frame,'more than 1 laser detected',(50,50),cv2.FONT_HERSHEY_COMPLEX_SMALL,0.6,255)

        else:
            # x, y, radius
            # x az chap and y az bala 
            x = circles[0][0][0]
            y = circles[0][0][1]
            # print('X:',x)
            # print('Y:',y)
            X_axis.append(x)
            Y_axis.append(y)

            circles = np.round(circles[0, :]).astype("int")
            cv2.circle(output_frame, center=(circles[0, 0], circles[0, 1]), radius=circles[0, 2], color=(0, 255, 0), thickness=2)
            cv2.putText(output_frame,'laser detected',(50,50),cv2.FONT_HERSHEY_COMPLEX_SMALL,0.6,255)
    

    cv2.imshow('frame', output_frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print('x:',X_axis)
        print('Y:',Y_axis)
        break

cv2.destroyAllWindows()

plt.scatter(X_axis,Y_axis,s = 1)
plt.show()

