#!/home/shannon/miniconda2/envs/cvbot/bin/python
#-*- coding: utf-8 -*-　　　←表示使用 utf-8 編碼
import cv2
import sys
import numpy as np
from matplotlib import pyplot as plt


def readImagesAndTimes(image_num,image_quality):
    # List of chosen image
    chosenImgs=[]
    filename=0
    path=""
    format=""
    tolerate=0
    pyramid_level=0
    if image_num == "robotics_corner":
        chosenImgs = range(22)
        filename = 57
        tolerate = 2
        if image_quality == 0:
            path="../test_img/Robotics_Corner/DSC098"
            format=".jpg"
            pyramid_level=5
        elif image_quality == 1:
            path="../raw_img/Robotics_Corner/DSC098"
            format=".JPG"
            pyramid_level=5
    elif image_num == "robot_power":
        chosenImgs = [7,11,13,16,18]
        filename = 23
        tolerate = 20
        if image_quality == 0:
            path="../test_img/Robot_Power/DSC099"
            format=".jpg"
            pyramid_level=5
        elif image_quality == 1:
            path="../raw_img/Robot_Power/DSC099"
            format=".JPG"
            pyramid_level=5
    # List of exposure times
    ctimes = []
    times = np.array(np.loadtxt("../raw_img/img_shutter_float.txt"), dtype=np.float32)
    for i in chosenImgs: ctimes.append(times[i])
    ctimeSet = np.array(ctimes)
    # List of images
    cimages = []
    for chosenImg in chosenImgs:
        fullfilename = filename+chosenImg
        fullpath = "{}{}{}".format(path,str(fullfilename),format)
        img = cv2.imread(fullpath)
        cimages.append(img)
    cimgSet = np.array(cimages)
    # Plot original images
    fig=plt.figure()
    fig.suptitle('original images from different exposures')
    for i,chosenImg in enumerate(chosenImgs):
        image=cimgSet[i,:,:,:]
        image_rgb=image[:,:,::-1]
        subfig = plt.subplot(len(chosenImgs),1,i+1)
        subfig.imshow(image_rgb)
    print "cimgSet ",cimgSet.shape; print "ctimeSet ",ctimeSet.shape
    return cimgSet,ctimeSet,tolerate,pyramid_level


def alignmentImages(imgSet,times,tolerate,pyramid_level):
    # take only green channel of images (or gray scale)
    imgSet_green = imgSet[:,:,:,1]
    # generate median
    img_median_list=[]
    for i,img in enumerate(imgSet_green):
        median = np.median(img)
        img_median_list.append(median)
    img_median = np.array(img_median_list)
    # plot image pyramids
    fig2=plt.figure()
    fig2.suptitle('image pyramids')
    # find the offset of each image
    for i,img in enumerate(imgSet_green):
        img_mtb = cv2.threshold(img, img_median[i], 255, cv2.THRESH_BINARY)[1]
        img_eb = cv2.inRange(img, img_median[i]-tolerate, img_median[i]+tolerate) # using the number 4 in paper casue a bad performance in my robot_power cases
        subfig = plt.subplot(2,22, i+1)
        subfig.imshow(img_mtb, cmap="gray")
        subfig = plt.subplot(2,22, i+22+1)
        subfig.imshow(img_eb, cmap="gray")
    return ""


def obtainCRF(imgSet_aligned,times):
    calibrateDebevec = cv2.createCalibrateDebevec()
    responseDebevec = calibrateDebevec.process(imgSet_aligned,times)
    return responseDebevec


def mergeImgAsHdr(CRF,imgSet_aligned,times):
    mergeDebevec = cv2.createMergeDebevec()
    hdrDevec = mergeDebevec.process(imgSet_aligned,times,CRF)
    return hdrDevec


def toneMappingReinhard(hdrImg):
    tonemapReinhard = cv2.createTonemapReinhard(0.9,4,1,0)
    ldrReinhard = tonemapReinhard.process(hdrImg)
    return ldrReinhard


def main():
    image_num = sys.argv[1]
    image_quality = int(sys.argv[2])

    imgSet,times,tolerate,pyramid_level = readImagesAndTimes(image_num,image_quality)
    imgSet_aligned = alignmentImages(imgSet,times,tolerate,pyramid_level)
    plt.show()

if __name__ == '__main__':
    main()
