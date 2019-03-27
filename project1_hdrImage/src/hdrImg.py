#!/home/shannon/miniconda2/envs/cvbot/bin/python
#-*- coding: utf-8 -*-　　　←表示使用 utf-8 編碼
import cv2
import numpy as np
from matplotlib import pyplot as plt

def readImagesAndTimes():
    # List of exposure times
    times = np.array(np.loadtxt("../raw_img/img_shutter_float.txt"), dtype=np.float32)[4:22]
    # List of image filenames
    images = []
    for fileNum in range(22):
        filename = 23+fileNum
        #filename = 57+fileNum
        path = "../test_img/image4/DSC099{}.jpg".format(str(filename))
        #path = "../raw_img/image4/DSC099{}.JPG".format(str(filename))
        #path = "../test_img/image1/DSC098{}.jpg".format(str(filename))
        img = cv2.imread(path)
        images.append(img)
    imgSet = np.array(images)
    imgSet_less=imgSet[4:22,:,:,:]

    fig=plt.figure()
    fig.suptitle('original')
    for i,time in enumerate(times):
        image=imgSet_less[i,:,:,:]
        image_rgb=image[:,:,::-1]
        subfig = plt.subplot(3,6,i+1)
        subfig.imshow(image_rgb)

    return imgSet_less,times

def alignmentImages(imgSet,times):
    alinMTB = cv2.createAlignMTB()
    alinMTB.process(imgSet,imgSet)
    imgSet_aligned=imgSet

    fig2=plt.figure()
    fig2.suptitle('aligned')
    for i,time in enumerate(times):
        image=imgSet_aligned[i,:,:,:]
        image_rgb=image[:,:,::-1]
        subfig = plt.subplot(3,6,i+1)
        subfig.imshow(image_rgb)

    return imgSet_aligned

def obtainCRF(imgSet_aligned,times):
    calibrateDebevec = cv2.createCalibrateDebevec()
    responseDebevec = calibrateDebevec.process(imgSet_aligned,times)

    fig3=plt.figure()
    fig3.suptitle('CRF')
    plt.plot(range(256),responseDebevec[:,0,0],c='b')
    plt.plot(range(256),responseDebevec[:,0,1],c='g')
    plt.plot(range(256),responseDebevec[:,0,2],c='r')

    return responseDebevec

def mergeImgAsHdr(CRF,imgSet_aligned,times):
    mergeDebevec = cv2.createMergeDebevec()
    hdrDevec = mergeDebevec.process(imgSet_aligned,times,CRF)
    cv2.imwrite("myFirstHdrImg.hdr",hdrDevec)
    return hdrDevec

def main():
    n=2
    imgSet,times = readImagesAndTimes()
    print "imgSet ",imgSet.shape
    print "times ",times.shape, "\n"
    imgSet_aligned = alignmentImages(imgSet,times)
    print "imgSet_aligned ",imgSet_aligned.shape, "\n"
    CRF = obtainCRF(imgSet_aligned,times)
    print "CRF ",CRF.shape, CRF,"\n"
    hdrImg = mergeImgAsHdr(CRF,imgSet_aligned,times)
    print "hdrImg ",hdrImg.shape,"\n"

    plt.show()

if __name__ == '__main__':
    main()
