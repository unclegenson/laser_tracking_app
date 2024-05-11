# import cv2
# import numpy as np
# import requests
# import imutils



# url = "http://192.168.1.102:8080/shot.jpg"
# # Load image


# while True:
#     img_resp = requests.get(url) 
#     img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8) 
#     captured_frame = cv2.imdecode(img_arr, -1) 
#     captured_frame = imutils.resize(captured_frame, width=1000, height=1800)
#     output_frame = captured_frame.copy()
#     captured_frame_bgr = cv2.cvtColor(captured_frame, cv2.COLOR_BGRA2BGR)

#     captured_frame_bgr = cv2.medianBlur(captured_frame_bgr, 3)
#     captured_frame_lab = cv2.cvtColor(captured_frame_bgr, cv2.COLOR_BGR2Lab)


#     img = cv2.GaussianBlur(captured_frame_lab, (5, 5), 0)

# # Apply Hough Circle Transform
#     circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 1, 20, param1=50, param2=30, minRadius=0, maxRadius=0)

#     # Convert the (x, y) coordinates and radius of the circles to integers
#     circles = np.round(circles[0, :]).astype("int")

#     # Draw circles on the original image
#     for (x, y, r) in circles:
#         cv2.circle(img, (x, y), r, (0, 255, 0), 2)

#     cv2.imshow('frame', captured_frame)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break


# cv2.destroyAllWindows()

import cv2
import numpy as np

# Load image
img = cv2.imread('c1.jpg', 0)

# Blur image
img = cv2.GaussianBlur(img, (5, 5), 0)

# Apply Hough Circle Transform
circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 1, 20, param1=50, param2=30, minRadius=20, maxRadius=70)

# Convert the (x, y) coordinates and radius of the circles to integers
circles = np.round(circles[0, :]).astype("int")

# Draw circles on the original image
for (x, y, r) in circles:
    cv2.circle(img, (x, y), r, (0, 255, 0), 2)

# Display the image
cv2.imshow("Detected Circles", img)
cv2.waitKey(0)
cv2.destroyAllWindows()