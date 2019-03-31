#!/home/shannon/miniconda2/envs/cvbot/bin/python
#-*- coding: utf-8 -*-　　　←表示使用 utf-8 編碼
import cv2
import sys
import numpy as np
from matplotlib import pyplot as plt

final_offset=[0,0]
fig=plt.figure()
fig.suptitle('original')
i=1
img = cv2.imread("../test_img/Robotics_Corner/DSC09866.jpg")[:,:,0]
print img.shape

level=5
img_scaled = cv2.pyrDown(img)
plt.imshow(img_scaled,cmap="gray")

img_median = np.median(img_scaled)
img_mtb = cv2.threshold(img_scaled, img_median, 255, cv2.THRESH_BINARY)[1]
print img_mtb
img_eb = cv2.inRange(img_scaled, img_median-4, img_median+4)
print img_eb
img_diff = np.logical_xor(img_mtb,img_mtb)
error = np.sum(img_diff)
print error
img_diff_filtered = np.logical_and(img_diff,img_eb)
error_filtered = np.sum(img_diff_filtered)
print error_filtered

plt.show()
