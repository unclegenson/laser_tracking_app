# import cv2
# import numpy as np

# cap = cv2.VideoCapture(0)

# while (1):

    
    
#     ret,img1 =  cap.read()

#     hsv = cv2.cvtColor(img1,cv2.COLOR_BGR2HSV)

#     #lower red
#     lower_red = np.array([0,50,50])
#     upper_red = np.array([10,255,255])

#     #upper red
#     lower_red2 = np.array([70,50,50])
#     upper_red2 = np.array([80,255,255])

#     mask = cv2.inRange(hsv, lower_red, upper_red)
#     res = cv2.bitwise_and(img1,img1, mask= mask)
#     mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
#     res2 = cv2.bitwise_and(img1,img1, mask= mask2)
#     img4 = cv2.add(res,res2)

#     cv2.imshow('res4',img4)

#     moments = cv2.moments(hsv[:, :, 2])
#     x = int(moments['m10'] / moments['m00'])
#     y = int(moments['m01'] / moments['m00'])
#     print('x:',x)
#     print('y:',y)

#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# cap.release()
# cv2.destroyAllWindows()



import cv2
from matplotlib import pyplot as plt
import numpy as np
 
 
file = r'C:\Users\Mahdi\Downloads\Telegram Desktop\photo_2024-03-18_14-47-56.jpg'

# Load the image
image = cv2.imread(file)
 
hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

lower_red = np.array([0, 100, 100])
upper_red = np.array([10, 255, 255])

mask = cv2.inRange(hsv_image, lower_red, upper_red)

kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

for contour in contours:
    x, y, w, h = cv2.boundingRect(contour)
    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 3)

plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
plt.show()