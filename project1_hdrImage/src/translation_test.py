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
img = cv2.imread("../test_img/image1_/DSC09866.jpg")[:,:,0]
print img.shape
for x_offset in [-100,0,100]:
    for y_offset in [-100,0,100]:
        offset = [x_offset+final_offset[0],y_offset+final_offset[1]]
        print offset
        translation_matrix = np.float32([ [1,0,offset[0]], [0,1,offset[1]] ])
        img_translation = cv2.warpAffine(img, translation_matrix, (img.shape[1],img.shape[0]))
        subfig = plt.subplot(3,3,i)
        subfig.imshow(img_translation, cmap='gray')
        i+=1
plt.show()
