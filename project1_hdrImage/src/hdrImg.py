#!/home/shannon/miniconda2/envs/cvbot/bin/python
#-*- coding: utf-8 -*-　　　←表示使用 utf-8 編碼
import cv2
import numpy as np
from matplotlib import pyplot as plt

def readImagesAndTimes():
    # List of exposure times
    times = np.array(np.loadtxt("../raw_img/img_shutter_float.txt"), dtype=np.float32)[0:22]
    # List of image filenames
    images = []
    for fileNum in range(22):
        #filename = 23+fileNum
        filename = 57+fileNum
        #path = "../test_img/image4/DSC099{}.jpg".format(str(filename))
        #path = "../raw_img/image4/DSC099{}.JPG".format(str(filename))
        #path = "../test_img/image1/DSC098{}.jpg".format(str(filename))
        path = "../raw_img/image1/DSC098{}.JPG".format(str(filename))
        img = cv2.imread(path)
        images.append(img)
    imgSet = np.array(images)
    imgSet_less=imgSet[0:22,:,:,:]

    '''fig=plt.figure()
    fig.suptitle('original')
    for i,time in enumerate(times):
        image=imgSet_less[i,:,:,:]
        image_rgb=image[:,:,::-1]
        subfig = plt.subplot(2,11,i+1)
        subfig.imshow(image_rgb)'''
    return imgSet_less,times

def alignmentImages(imgSet,times):
    alinMTB = cv2.createAlignMTB()
    alinMTB.process(imgSet,imgSet)
    imgSet_aligned=imgSet

    '''fig2=plt.figure()
    fig2.suptitle('aligned')
    for i,time in enumerate(times):
        image=imgSet_aligned[i,:,:,:]
        image_rgb=image[:,:,::-1]
        subfig = plt.subplot(2,11,i+1)
        subfig.imshow(image_rgb)'''
    return imgSet_aligned

def obtainCRF(imgSet_aligned,times):
    calibrateDebevec = cv2.createCalibrateDebevec()
    responseDebevec = calibrateDebevec.process(imgSet_aligned,times)

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

    ldrDrago_rgb=ldrDrago[:,:,::-1]
    subfig = plt.subplot(2,2,1)
    subfig.set_title("Drago")
    subfig.imshow(ldrDrago_rgb)
    return ldrDrago

def toneMappingDurand(hdrImg):
    tonemapDurand = cv2.createTonemapDurand(0.45,3,1.1,1,1)
    ldrDurand = tonemapDurand.process(hdrImg)
    ldrDurand = 3* ldrDurand

    ldrDurand_rgb=ldrDurand[:,:,::-1]
    subfig = plt.subplot(2,2,2)
    subfig.set_title("Durand")
    subfig.imshow(ldrDurand_rgb)
    return ldrDurand

def toneMappingReinhard(hdrImg):
    tonemapReinhard = cv2.createTonemapReinhard(1.35,0.5,0.5,1)
    ldrReinhard = tonemapReinhard.process(hdrImg)

    ldrReinhard_rgb=ldrReinhard[:,:,::-1]
    subfig = plt.subplot(2,2,3)
    subfig.set_title("Reinhard")
    subfig.imshow(ldrReinhard_rgb)
    return ldrReinhard

def toneMappingMantiuk(hdrImg):
    tonemapMantiuk = cv2.createTonemapMantiuk(2.8,0.9,1.5)
    ldrMantiuk = tonemapMantiuk.process(hdrImg)

    ldrMantiuk_rgb=ldrMantiuk[:,:,::-1]
    subfig = plt.subplot(2,2,4)
    subfig.set_title("Mantiuk")
    subfig.imshow(ldrMantiuk_rgb)
    return ldrMantiuk

def main():
    n=2
    imgSet,times = readImagesAndTimes()
    print "imgSet ",imgSet.shape
    print "times ",times.shape, "\n"
    imgSet_aligned = alignmentImages(imgSet,times)
    print "imgSet_aligned ",imgSet_aligned.shape, "\n"
    CRF = obtainCRF(imgSet_aligned,times)
    print "CRF ",CRF.shape,"\n"
    hdrImg = mergeImgAsHdr(CRF,imgSet_aligned,times)
    print "hdrImg ",hdrImg.shape,hdrImg,"\n"

    fig4=plt.figure()
    fig4.suptitle('HDR images')
    ldrImgDrago = toneMappingDrago(hdrImg)
    ldrImgDurand = toneMappingDurand(hdrImg)
    ldrImgReinhard = toneMappingReinhard(hdrImg)
    ldrImgMantiuk = toneMappingMantiuk(hdrImg)

    plt.show()

if __name__ == '__main__':
    main()
