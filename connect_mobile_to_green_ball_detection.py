# import the necessary packages
from collections import deque
from imutils.video import VideoStream
import numpy as np
import argparse
import cv2
import imutils
import time
import requests

url = "http://192.168.1.102:8080/shot.jpg"

pts = deque()
radiuses = deque()

greenLower = (29, 86, 6)
greenUpper = (64, 255, 255)

counter = 0
(dX, dY) = (0, 0)
direction = ""

time.sleep(2.0)

while True:

	img_resp = requests.get(url) 
	img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8)
	captured_frame = cv2.imdecode(img_arr, -1)

	# resize the frame, blur it, and convert it to the HSV
	# color space
	frame = imutils.resize(captured_frame, width=600)
	blurred = cv2.GaussianBlur(captured_frame, (11, 11), 0)
	hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
	# construct a mask for the color "green", then perform
	# a series of dilations and erosions to remove any small
	# blobs left in the mask
	mask = cv2.inRange(hsv, greenLower, greenUpper)
	mask = cv2.erode(mask, None, iterations=2)
	mask = cv2.dilate(mask, None, iterations=2)
	# find contours in the mask and initialize the current
	# (x, y) center of the ball
	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)
	center = None

        
	# only proceed if at least one contour was found
	if len(cnts) > 0:
		# find the largest contour in the mask, then use
		# it to compute the minimum enclosing circle and
		# centroid
		c = max(cnts, key=cv2.contourArea)
		((x, y), radius) = cv2.minEnclosingCircle(c)
		M = cv2.moments(c)
		center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
		# only proceed if the radius meets a minimum size
		if radius > 10:
			# then update the list of tracked points
			pts.appendleft(center)
			radiuses.appendleft(radius)
	# loop over the set of tracked points

	# for i in np.arange(1, len(pts)):
			
	# 	if pts[i - 1] is None or pts[i] is None:
	# 		continue
		
	# 	if counter >= 10 and i == 1 and pts[0] is not None:

	# 		dX = pts[0][0] - pts[i][0]
	# 		dY = pts[0][1] - pts[i][1]
	# 		(dirX, dirY) = ("", "")

	# 		if np.abs(dX) > 20:
	# 			dirX = "East" if np.sign(dX) == 1 else "West"

	# 		if np.abs(dY) > 20:
	# 			dirY = "North" if np.sign(dY) == -1 else "South"

	# 		if dirX != "" and dirY != "":
	# 			direction = "{}-{}".format(dirY, dirX)

	# 		else:
	# 			direction = dirX if dirX != "" else dirY
	for i in np.arange(1, len(radiuses)):
		
		if radiuses[i - 1] is None or radiuses[i] is None:
			continue
			
		if counter >= 10 and i == 1 and radiuses[0] is not None:

			dX = radiuses[0] - radiuses[i]
			dirX = ''
			if np.abs(dX) > 10:
				dirX = "Forward" if np.sign(dX) == 1 else "Backward"
				
			if dirX != "" :
				direction = "{}".format(dirX)

			else:
				direction = dirX if dirX != "" else ''

	cv2.putText(frame, direction, (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
		0.65, (0, 0, 255), 3)
	cv2.putText(frame, "dx: {}, dy: {}".format(dX, dY),
		(10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX,
		0.35, (0, 0, 255), 1)

	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF
	counter += 1

	if key == ord("q"):
		break

# close all windows
cv2.destroyAllWindows()
