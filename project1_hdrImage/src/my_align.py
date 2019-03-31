#!/home/shannon/miniconda2/envs/cvbot/bin/python
#-*- coding: utf-8 -*-
import cv2
import sys
import numpy as np
from matplotlib import pyplot as plt


def readImagesAndTimes(image_num,image_quality):
    # Pick the images and parameters we want
    chosenImgs, fileNumber, path, format = [], 0, "", ""
    if image_num == "robotics_corner":
        #chosenImgs = [1,5,8,13,16] # bad chosen, judging from mtb and eb
        chosenImgs, fileNumber = [7,9,12,15,17], 57
        if image_quality == 0:
            path, format, pyramid_level = "../test_img/Robotics_Corner/DSC098", ".jpg", 5
        elif image_quality == 1:
            path, format, pyramid_level = "../raw_img/Robotics_Corner/DSC098", ".JPG", 6
    elif image_num == "robot_power":
        chosenImgs, fileNumber = [7,11,13,16,18], 23
        if image_quality == 0:
            path, format, pyramid_level = "../test_img/Robot_Power/DSC099", ".jpg", 5
        elif image_quality == 1:
            path, format, pyramid_level = "../raw_img/Robot_Power/DSC099", ".JPG", 6
    # Create ndarray of exposure times
    times = np.array(np.loadtxt("../raw_img/img_shutter_float.txt"), dtype=np.float32)
    ctimes = []
    for i in chosenImgs: ctimes.append(times[i])
    ctimeSet = np.array(ctimes)
    # Create ndarray of images
    cimages = []
    for chosenImg in chosenImgs:
        fullFileNumber = fileNumber+chosenImg
        fullpath = "{}{}{}".format(path,str(fullFileNumber),format)
        img = cv2.imread(fullpath)
        cimages.append(img)
    cimgSet = np.array(cimages)
    # Plot original images, Pring info
    fig=plt.figure().suptitle('original images from different exposures')
    for i,chosenImg in enumerate(chosenImgs):
        image=cimgSet[i,:,:,:]
        image_rgb=image[:,:,::-1]
        subfig = plt.subplot(len(chosenImgs),1,i+1).imshow(image_rgb)
    print "cimgSet ",cimgSet.shape; print "ctimeSet ",ctimeSet.shape
    return cimgSet,ctimeSet,pyramid_level


def alignmentImages(imgSet,times,pyramid_level):
    # take only green channel of images (or gray scale -> performance is not so good)
    imgSet_green = imgSet[:,:,:,1]
    '''imgSet_gray_list = []
    for img in imgSet:
        imgt_gray = (19*np.array(img[:,:,0]).astype(np.int16) + 183*np.array(img[:,:,1]).astype(np.int16) + 54*np.array(img[:,:,2]).astype(np.int16)) / 256
        imgSet_gray_list.append(imgt_gray)
    imgSet_green = np.array(imgSet_gray_list)'''
    # generate image pyramid for every image as "num of images" by "pyramid level" array
    img_pyramids = []
    for i,img in enumerate(imgSet_green):
        img_pyramid, level = [img], img
        for i in range(pyramid_level-1):
            level = cv2.pyrDown(level)
            img_pyramid.insert(0,level)
        img_pyramids.append(img_pyramid)
    # plot image pyramids and print info
    fig2=plt.figure().suptitle('image pyramids')
    for i,pyramid in enumerate(range(len(imgSet_green))):
        for j,level in enumerate(range(pyramid_level)):
            subfig = plt.subplot(len(imgSet_green), pyramid_level, j+1+i*pyramid_level).imshow(img_pyramids[i][j], cmap="gray")
    print "img_numbers=",len(imgSet),"pyramid_level=",pyramid_level,"img_pyramids", np.array(img_pyramids).shape
    # generate median for every image
    img_median = [np.median(img) for img in imgSet_green]
    # find the offset of each image
    final_offsets = []
    for i,image_pyramid in enumerate(range(len(imgSet_green))):
        final_offset = [0, 0]
        for j,level in enumerate(range(pyramid_level)):
            # generate median threshold bitmap and exclusive bitmap
            img_mtb = cv2.threshold(img_pyramids[i][j], img_median[i], 255, cv2.THRESH_BINARY)[1]
            img_eb = cv2.inRange(img_pyramids[i][j], img_median[i]-10, img_median[i]+10) # using the number 4 in paper casue a bad performance in my robot_power cases
            ref_mtb = cv2.threshold(img_pyramids[0][j], img_median[0], 255, cv2.THRESH_BINARY)[1]
            # find the min diff step in 9 neighbors
            level_offset = [0,0] # the direction of this level patch want to move
            diff = float('Inf')
            for x_offset in [-1,0,1]:
                for y_offset in [-1,0,1]:
                    offset = [x_offset + final_offset[0], y_offset + final_offset[1]]
                    translation_matrix = np.float32([ [1,0,offset[0]], [0,1,offset[1]] ])
                    img_translation = cv2.warpAffine(img_mtb, translation_matrix, (img_mtb.shape[1],img_mtb.shape[0]))
                    img_diff = np.logical_xor(ref_mtb,img_translation)
                    img_diff_filtered = np.logical_and(img_diff,img_eb)
                    diff_temp = np.sum(img_diff_filtered)
                    if diff_temp < diff: diff, level_offset = diff_temp, offset
            final_offset = level_offset # pass offset to next level of pyramid
        final_offsets.append(final_offset)
    print "final_offsets",final_offsets
    # translate images by final_offsets
    img_translation_list = []
    for i, img in enumerate(imgSet):
        offset = final_offsets[i]
        translation_matrix = np.float32([ [1,0,offset[0]], [0,1,offset[1]] ])
        img_translation = cv2.warpAffine(img, translation_matrix, (img.shape[1],img.shape[0]))
        img_translation_list.append(img_translation)
    img_translation = np.array(img_translation_list)
    # Plot translated images, prnt info
    fig3=plt.figure().suptitle('translated images by MTB algorithm')
    for i,img in enumerate(img_translation):
        img_rgb=img[:,:,::-1]
        subfig = plt.subplot(len(img_translation),1,i+1).imshow(img_rgb)
    print "imgSet_aligned ",img_translation.shape
    return img_translation


# bulit-in function
def obtainCRF(imgSet_aligned,times):
    calibrateDebevec = cv2.createCalibrateDebevec()
    responseDebevec = calibrateDebevec.process(imgSet_aligned, times)
    print "CRF ",responseDebevec.shape
    return responseDebevec


# bulit-in function
def mergeImgAsHdr(CRF,imgSet_aligned,times):
    mergeDebevec = cv2.createMergeDebevec()
    hdrDevec = mergeDebevec.process(imgSet_aligned,times, CRF)
    print "hdrImg ",hdrDevec.shape
    return hdrDevec


# bulit-in function
def toneMappingReinhard(hdrImg):
    tonemapReinhard = cv2.createTonemapReinhard(0.9, 4, 1, 0) # gama, intensity, light_adapt, color_adapt
    ldrReinhard = tonemapReinhard.process(hdrImg)
    return ldrReinhard


def main():
    image_num, image_quality = sys.argv[1], int(sys.argv[2])
    imgSet,times,pyramid_level = readImagesAndTimes(image_num,image_quality)
    imgSet_aligned = alignmentImages(imgSet,times,pyramid_level)

    # generate hdr by bulit in function ( w/ aligned)
    CRF = obtainCRF(imgSet_aligned,times)
    hdrImg = mergeImgAsHdr(CRF,imgSet_aligned,times)
    ldrImgReinhard = toneMappingReinhard(hdrImg)
    # Plot hdr images
    ldrImgReinhard_rgb=ldrImgReinhard[:,:,::-1]
    fig4=plt.figure().suptitle('HDR image w/ aligned')
    plt.imshow(ldrImgReinhard_rgb)

    # generate hdr by bulit in function ( w/o aligned)
    CRF = obtainCRF(imgSet,times)
    hdrImg = mergeImgAsHdr(CRF,imgSet,times)
    ldrImgReinhard = toneMappingReinhard(hdrImg)
    # Plot hdr images
    ldrImgReinhard_rgb=ldrImgReinhard[:,:,::-1]
    fig5=plt.figure().suptitle('HDR image w/o aligned')
    plt.imshow(ldrImgReinhard_rgb)

    plt.show()

if __name__ == '__main__':
    main()
