import cv2
import numpy as np
img1 = cv2.imread('0.jpg')
img2 = cv2.imread('1.jpg')
img1_h, img1_w = img1.shape[:2]
img2_h, img2_w = img2.shape[:2]
print img1.shape, img1_h, img1_w
print img2.shape, img2_h, img2_w

new_img = np.zeros((img1_h+16,img1_w+img2_w-78,3),dtype=np.uint8)
print new_img.shape
print new_img[16:][:][:].shape
print new_img[:img2_h][:][:].shape

cv2.imwrite('0Translation.png', new_img)
cv2.waitKey()
