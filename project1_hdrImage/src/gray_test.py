#!/home/shannon/miniconda2/envs/cvbot/bin/python
#-*- coding: utf-8 -*-　　　←表示使用 utf-8 編碼
import cv2
import sys
import numpy as np
from matplotlib import pyplot as plt

img2 = cv2.imread("../test_img/Robotics_Corner/DSC09866.jpg")
print 19*np.array(img2[:,:,0]).astype(np.int16)
print 183*np.array(img2[:,:,1]).astype(np.int16)
print 54*np.array(img2[:,:,2]).astype(np.int16)
imgSet_green = (19*np.array(img2[:,:,0]).astype(np.int16) + 183*np.array(img2[:,:,1]).astype(np.int16) + 54*np.array(img2[:,:,2]).astype(np.int16)) / 256
print imgSet_green
plt.imshow(imgSet_green,cmap="gray")

plt.show()
