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
    if image_num == 1:
        chosenImgs = [1,5,8,13,16]
        filename = 57
        if image_quality == 0:
            path="../test_img/image1_/DSC098"
            format=".jpg"
        elif image_quality == 1:
            path="../raw_img/image1/DSC098"
            format=".JPG"
    elif image_num == 4:
        chosenImgs = [7,11,13,16,18]
        filename = 23
        if image_quality == 0:
            path="../test_img/image4_/DSC099"
            format=".jpg"
        elif image_quality == 1:
            path="../raw_img/image4/DSC099"
            format=".JPG"
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
    '''fig=plt.figure()
    fig.suptitle('original')
    for i,chosenImg in enumerate(chosenImgs):
        image=cimgSet[i,:,:,:]
        image_rgb=image[:,:,::-1]
        subfig = plt.subplot(1,len(chosenImgs),i+1)
        subfig.imshow(image_rgb)'''
    return cimgSet,ctimeSet


def alignmentImages(imgSet,times):
    alinMTB = cv2.createAlignMTB()
    alinMTB.process(imgSet,imgSet)
    imgSet_aligned=imgSet
    # Plot aligned images
    '''fig2=plt.figure()
    fig2.suptitle('aligned')
    for i,time in enumerate(times):
        image=imgSet_aligned[i,:,:,:]
        image_rgb=image[:,:,::-1]
        subfig = plt.subplot(1,len(times),i+1)
        subfig.imshow(image_rgb)'''
    return imgSet_aligned


def obtainCRF(imgSet_aligned,times):
    calibrateDebevec = cv2.createCalibrateDebevec()
    responseDebevec = calibrateDebevec.process(imgSet_aligned,times)
    # Plot CRF
    '''fig3=plt.figure()
    fig3.suptitle('CRF')
    plt.plot(range(256),responseDebevec[:,0,0],c='b')
    plt.plot(range(256),responseDebevec[:,0,1],c='g')
    plt.plot(range(256),responseDebevec[:,0,2],c='r')'''
    return responseDebevec


def mergeImgAsHdr(CRF,imgSet_aligned,times):
    mergeDebevec = cv2.createMergeDebevec()
    hdrDevec = mergeDebevec.process(imgSet_aligned,times,CRF)
    return hdrDevec


def toneMappingDrago(hdrImg):
    tonemapDrago = cv2.createTonemapDrago(0.75,0.7)
    ldrDrago = tonemapDrago.process(hdrImg)
    ldrDrago = 3* ldrDrago
    # Plot hdr images
    ldrDrago_rgb=ldrDrago[:,:,::-1]
    subfig = plt.subplot(2,2,1)
    subfig.set_title("Drago")
    subfig.imshow(ldrDrago_rgb)
    return ldrDrago


def toneMappingDurand(hdrImg):
    tonemapDurand = cv2.createTonemapDurand(0.45,3,1.1,1,1)
    ldrDurand = tonemapDurand.process(hdrImg)
    ldrDurand = 3* ldrDurand
    # Plot hdr images
    ldrDurand_rgb=ldrDurand[:,:,::-1]
    subfig = plt.subplot(2,2,2)
    subfig.set_title("Durand")
    subfig.imshow(ldrDurand_rgb)
    return ldrDurand


def toneMappingReinhard(hdrImg):
    tonemapReinhard = cv2.createTonemapReinhard(0.9,4,1,0)
    ldrReinhard = tonemapReinhard.process(hdrImg)
    # Plot hdr images
    ldrReinhard_rgb=ldrReinhard[:,:,::-1]
    subfig = plt.subplot(2,2,3)
    subfig.set_title("Reinhard")
    subfig.imshow(ldrReinhard_rgb)
    return ldrReinhard


def toneMappingMantiuk(hdrImg):
    tonemapMantiuk = cv2.createTonemapMantiuk(2.8,0.9,1.5)
    ldrMantiuk = tonemapMantiuk.process(hdrImg)
    # Plot hdr images
    ldrMantiuk_rgb=ldrMantiuk[:,:,::-1]
    subfig = plt.subplot(2,2,4)
    subfig.set_title("Mantiuk")
    subfig.imshow(ldrMantiuk_rgb)
    return ldrMantiuk


def main():
    image_num = int(sys.argv[1])
    image_quality = int(sys.argv[2])
    imgSet,times = readImagesAndTimes(image_num,image_quality)
    print "imgSet ",imgSet.shape; print "times ",times.shape
    imgSet_aligned = alignmentImages(imgSet,times)
    print "imgSet_aligned ",imgSet_aligned.shape
    CRF = obtainCRF(imgSet_aligned,times)
    print "CRF ",CRF.shape
    hdrImg = mergeImgAsHdr(CRF,imgSet_aligned,times)
    print "hdrImg ",hdrImg.shape

    # Plot hdr images
    fig4=plt.figure()
    fig4.suptitle('HDR images')
    #ldrImgDrago = toneMappingDrago(hdrImg)
    #ldrImgDurand = toneMappingDurand(hdrImg)
    #ldrImgMantiuk = toneMappingMantiuk(hdrImg)
    ldrImgReinhard = toneMappingReinhard(hdrImg)
    # Save photo
    cv2.imwrite("img.jpg",ldrImgReinhard*255, [cv2.IMWRITE_JPEG_QUALITY,100])
    plt.show()


if __name__ == '__main__':
    main()
