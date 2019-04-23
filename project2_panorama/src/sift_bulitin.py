import numpy as np
import cv2

img = cv2.imread('test_img/dormitoryNight/DSC09994.jpg')
gray= cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

sift = cv2.xfeatures2d.SIFT_create()
kp, des = sift.detectAndCompute(gray,None)
print(kp,des)
#kp = sift.detect(gray,None)

img=cv2.drawKeypoints(gray,kp,img,flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
#img=cv2.drawKeypoints(gray,kp,img)

cv2.imshow("img",img)
cv2.waitKey()
