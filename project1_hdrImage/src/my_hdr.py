#!/home/shannon/miniconda2/envs/cvbot/bin/python
#-*- coding: utf-8 -*-
import cv2
import math
import sys
import numpy as np
from matplotlib import pyplot as plt
import random

def readImagesAndTimes(image_num,image_quality):
    # Pick the images and parameter s we want
    chosenImgs, fileNumber, path, format = [], 0, "", ""
    if image_num == "robotics_corner":
        #chosenImgs = [1,5,8,13,16] # bad chosen, judging from mtb and eb
        chosenImgs, fileNumber = [8,10,12,14,16], 57 #[3,5,9,13,20], 57
        if image_quality == 0:
            path, format, pyramid_level = "../test_img/Robotics_Corner/DSC098", ".jpg", 5
        elif image_quality == 1:
            path, format, pyramid_level = "../use_img/Robotics_Corner/DSC098", ".jpg", 5
            #path, format, pyramid_level = "../raw_img/Robotics_Corner/DSC098", ".JPG", 6
    elif image_num == "robot_power":
        chosenImgs, fileNumber = [7,11,13,16,18], 23
        if image_quality == 0:
            path, format, pyramid_level = "../test_img/Robot_Power/DSC099", ".jpg", 5
        elif image_quality == 1:
            path, format, pyramid_level = "../use_img/Robot_Power/DSC099", ".jpg", 5
            #path, format, pyramid_level = "../raw_img/Robot_Power/DSC099", ".JPG", 6
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
    # fig=plt.figure().suptitle('original images from different exposures')
    fig7=plt.figure().suptitle('original images')
    for i,chosenImg in enumerate(chosenImgs):
        image=cimgSet[i,:,:,:]
        image_rgb=image[:,:,::-1]
        subfig=plt.subplot(1,len(chosenImgs),i+1)
        subfig.imshow(image_rgb)
        subfig.set_title("exposureT:"+str(ctimeSet[i]))
    fig=plt.figure().suptitle('image alignment: origin -> pyramid -> mtb -> eb -> result')
    for i,chosenImg in enumerate(chosenImgs):
        image=cimgSet[i,:,:,:]
        image_rgb=image[:,:,::-1]
        plt.subplot(len(chosenImgs),pyramid_level+1+2+1,(pyramid_level+1+2+1)*i+1).imshow(image_rgb)
    print "cimgSet ",cimgSet.shape; print "ctimeSet ",ctimeSet.shape
    return cimgSet,ctimeSet,pyramid_level


# implementation of Greg Ward, Fast Robust Image Registration for Compositing High Dynamic Range Photographs from Hand-Held Exposures, jgt 2003.
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
    #fig2=plt.figure().suptitle('image pyramids')
    for i,pyramid in enumerate(range(len(imgSet_green))):
        for j,level in enumerate(range(pyramid_level)):
            plt.subplot(len(imgSet_green), pyramid_level+1+2+1, 1+(1+j)+i*(pyramid_level+1+2+1)).imshow(img_pyramids[i][j], cmap="gray")
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
            ref_mtb = cv2.threshold(img_pyramids[2][j], img_median[2], 255, cv2.THRESH_BINARY)[1]
            # plot mtb,eb of the highest level of pyramid
            if level==pyramid_level-1:
                plt.subplot(len(imgSet_green), pyramid_level+1+2+1, 1+pyramid_level+1+i*(pyramid_level+1+2+1)).imshow(img_mtb, cmap="gray")
                plt.subplot(len(imgSet_green), pyramid_level+1+2+1, 1+pyramid_level+2+i*(pyramid_level+1+2+1)).imshow(img_eb, cmap="gray")
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
    # fig3=plt.figure().suptitle('translated images by MTB algorithm')
    for i,img in enumerate(img_translation):
        img_rgb=img[:,:,::-1]
        plt.subplot(len(imgSet_green), pyramid_level+1+2+1, 1+pyramid_level+3+i*(pyramid_level+1+2+1)).imshow(img_rgb)
    # Plot translated images, prnt info
    fig8=plt.figure().suptitle('translated images by MTB algorithm')
    for i,img in enumerate(img_translation):
        img_rgb=img[:,:,::-1]
        plt.subplot(1,len(imgSet_green), 1+i).imshow(img_rgb)

    print "imgSet_aligned ",img_translation.shape
    return img_translation


# built-in method
def alignmentImages_cv2(imgSet,times):
    alinMTB = cv2.createAlignMTB()
    alinMTB.process(imgSet,imgSet)
    imgSet_aligned=imgSet
    return imgSet_aligned


# implementation of Paul E. Debevec, Jitendra Malik, Recovering High Dynamic Range Radiance Maps from Photographs, SIGGRAPH 1997.
# Correspond to original matlab code
# [g,lE] = gslove(Z,lt,l,w)
def obtainCRF(imgSet_aligned_channel,times):
    # find the parameters Z, lt, l, w
    lt = np.log(times)
    l = 30
    w = [ (z if z <= 0.5*255 else 255-z ) for z in range(256) ]
    #print "imgSet_aligned_channel ",imgSet_aligned_channel.shape
    #print "lt",lt ;print "l",l ;print "w",w
    randomPoints, Z_list = [], []
    for n in range(50):
        x = random.randint(0, imgSet_aligned_channel.shape[1]-1)
        y = random.randint(0, imgSet_aligned_channel.shape[2]-1)
        randomPoint = [x, y]
        randomPoints.append(randomPoint)
    for img in imgSet_aligned_channel:
        image_Zs = []
        for point in randomPoints:
            image_Zs.append(img[point[0]][point[1]])
        Z_list.append(image_Zs)
    Z = np.array(Z_list)
    #print "randomPoints", randomPoints
    #print "Z ",Z.shape, Z

    # start to solve g and lE
    n = 256 # intensity, 1 pixel 0~255
    exposures = np.size(Z, 0)
    pickedPoints = np.size(Z, 1)
    A = np.zeros(shape=(exposures*pickedPoints + n + 1, n + pickedPoints), dtype=np.float32)
    b = np.zeros(shape=(np.size(A,0), 1), dtype=np.float32)
    # Include the data−fitting equations
    k = 0 # start from first row
    for i in range(pickedPoints):
        for j in range(exposures):
            z = Z[j][i] # intensity
            wij = w[z] # weight
            A[k][z] = wij; A[k][n+i] = -wij # fill array A
            b[k] = wij*lt[j] # fill array B
            k += 1 # to next row
    # Fix the curve by setting its middle value to 0
    A[k][128] = 1; k += 1 # g(128)=0
    # Include the smoothness equations
    for i in range(1,255): # g''(z)=g(z-1)-2g(z)+g(z+1)
        A[k][i-1]   =    l*w[i]
        A[k][i] = -2*l*w[i]
        A[k][i+1] =    l*w[i]
        k += 1
    # least square solution using SVD
    x = np.linalg.lstsq(A, b,rcond=-1)[0]
    g, lE = x[:256], x[256:]
    return g, lE


def plotCRF(CRF):
    # plot response curve
    fig4=plt.figure().suptitle('Camera Response function curve')
    plt.plot(CRF[0], range(256), 'r','o')
    plt.plot(CRF[1], range(256), 'g','o')
    plt.plot(CRF[2], range(256), 'b','o')
    plt.ylabel('pixel intensity Z')
    plt.xlabel('g(Z) = log exposure X')


def generatelE(CRF,Z,lt,w):
    exposures, pixels = len(Z), len(Z[0])
    lEs=[]
    for i in range(pixels):
        numerator=0.0
        denominator=0.0
        for j in range(exposures):
            zij = Z[j][i]
            numerator += w[zij]*(CRF[zij] - lt[j])
            denominator += w[zij]
        lE = numerator / denominator if denominator > 0 else numerator
        lEs.append(lE)
    return lEs


def generateRadianceMap(imgSet_aligned,CRF,times):
    lt = np.log(times)
    w = [ (z if z <= 0.5*255 else 255-z ) for z in range(256) ]
    radianceMap = np.zeros((imgSet_aligned.shape[1],imgSet_aligned.shape[2],3), dtype=np.float32)
    for i in range(3): #rgb
        Z = [img.flatten().tolist() for img in imgSet_aligned[:,:,:,i]] # p pieces * n pixels
        lE = generatelE(CRF[i], Z, lt, w)
        radianceMap[:,:,i] = np.exp(lE).reshape(imgSet_aligned.shape[1],imgSet_aligned.shape[2])
    print "radianceMap",radianceMap.shape
    return radianceMap


def plotRadianceMap(radianceMap):
    fig6=plt.figure().suptitle('radiance color HDR image')
    plt.imshow(np.log(cv2.cvtColor(radianceMap, cv2.COLOR_BGR2GRAY)), cmap='jet')
    plt.colorbar()


# bulit-in tone-mapping function
def toneMappingDrago(hdrImg):
    tonemapDrago = cv2.createTonemapDrago(1.55,1.25,1.0)#robotics_corner
    ldrDrago = tonemapDrago.process(hdrImg)
    ldrDrago = 3* ldrDrago
    # Plot hdr images
    ldrDrago_rgb=ldrDrago[:,:,::-1]
    subfig = plt.subplot(2,2,1)
    subfig.set_title("Drago")
    subfig.imshow(ldrDrago_rgb)
    return ldrDrago
# bulit-in tone-mapping function
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
# bulit-in tone-mapping function
def toneMappingReinhard(hdrImg):
    tonemapReinhard = cv2.createTonemapReinhard(0.9,4,1,0) # gama, intensity, light_adapt, color_adapt
    ldrReinhard = tonemapReinhard.process(hdrImg)
    # Plot hdr images
    ldrReinhard_rgb=ldrReinhard[:,:,::-1]
    #fig5=plt.figure().suptitle('tone-mapped HDR image')
    #plt.imshow(ldrReinhard_rgb)
    subfig = plt.subplot(2,2,3)
    subfig.set_title("Reinhard")
    subfig.imshow(ldrReinhard_rgb)
    return ldrReinhard
# bulit-in tone-mapping function
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
    # read images and infos
    image_num, image_quality, align = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
    imgSet,times,pyramid_level = readImagesAndTimes(image_num,image_quality)

    # image alignment
    if (align==1): imgSet_aligned = alignmentImages(imgSet,times,pyramid_level)
    elif (align==0): imgSet_aligned = alignmentImages_cv2(imgSet,times)

    # Recover response curve
    CRF_r,lE_r = obtainCRF(imgSet_aligned[:,:,:,2],times)
    CRF_g,lE_g = obtainCRF(imgSet_aligned[:,:,:,1],times)
    CRF_b,lE_b = obtainCRF(imgSet_aligned[:,:,:,0],times)
    CRF=[CRF_b, CRF_g, CRF_r]
    plotCRF(CRF)

    # Generate my hdr img
    radianceMap = generateRadianceMap(imgSet_aligned,CRF,times)
    plotRadianceMap(radianceMap)
    cv2.imwrite(image_num+"_test.hdr",radianceMap)

    # Run 4 bulit-in tone-mapping
    fig8=plt.figure().suptitle('original images')
    ldrImgDrago = toneMappingDrago(radianceMap)
    ldrImgDurand = toneMappingDurand(radianceMap)
    ldrImgMantiuk = toneMappingMantiuk(radianceMap)
    ldrImgReinhard = toneMappingReinhard(radianceMap)

    # Save the best of them (ldrImgReinhard)
    cv2.imwrite(image_num+"_test.jpg",ldrImgReinhard*255, [cv2.IMWRITE_JPEG_QUALITY,100])
    cv2.imwrite(image_num+"_test2.jpg",ldrImgDrago*255, [cv2.IMWRITE_JPEG_QUALITY,100])

    plt.show()

if __name__ == '__main__':
    main()
