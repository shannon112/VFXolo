import sys
import numpy as np
import math
import matplotlib.pyplot as plt
import cv2
import multiprocessing as mp

import warpToCylinder as wtc
from siftdetector import sift_detector
from siftmatch import sift_matching
import stitch
import constant as const

if __name__ == '__main__':
    # read files
    image_dir = sys.argv[1]
    image_set = wtc.load_images(image_dir)
    focal_length = wtc.load_focal_length(image_dir)
    image_set_size, height, width, _ =  image_set.shape
    print 'image_set',image_set.shape, 'focal_length set',focal_length.shape
    sys.stdout.flush()

    # project to cylinder coordinate
    cylinder_projs = wtc.cylindrical_projection(image_set, focal_length)
    fig1=plt.figure().suptitle('cylindrical_projection')
    for i,cylinder_proj in enumerate(cylinder_projs):
        cylinder_proj_rgb = cylinder_proj[:,:,::-1]
        subfig = plt.subplot(2,math.ceil(image_set_size/2.),i+1)
        subfig.imshow(cylinder_proj_rgb)
        cv2.imwrite(str(i)+".jpg",cylinder_proj)

    # initail values
    stitched_image = cylinder_projs[0].copy() #most left one as initail
    shifts = [] #every shift between two nearby images
    feature_cache = [[], []] #store last image feature
    sift_threshold = 5
    sift_cutoff = 0.0003

    #stiching from left to right
    for i in range(1, image_set_size):
        print 'Computing ...... {}/{}'.format(str(i),str(image_set_size-1)); sys.stdout.flush()
        img1 = str(i-1)+".jpg"
        img2 = str(i)+".jpg"
        img1_cv = cylinder_projs[i-1].copy()
        img2_cv = cylinder_projs[i].copy()

        print ' | Reload features in previous image .... '; sys.stdout.flush()
        keypints1, descriptors1 = feature_cache
        if i==1: #first loop
            keypints1, descriptors1 = sift_detector(img1,sift_threshold)
        print ' | | | {} features are extracted'.format(str(len(descriptors1))); sys.stdout.flush()


        print ' | Find features in image #{} ... '.format(str(i+1)); sys.stdout.flush()
        keypints2, descriptors2 = sift_detector(img2,sift_threshold)
        feature_cache = [keypints2, descriptors2]
        print ' | | | {} features are extracted'.format(str(len(descriptors2))); sys.stdout.flush()


        print ' | Feature matching .... '; sys.stdout.flush()
        matched_pairs = sift_matching(img1, img2 , keypints1, descriptors1, keypints2, descriptors2, sift_cutoff)
        print ' | | ' + str(len(matched_pairs)) + ' features matched.'; sys.stdout.flush()

        print ' | Find best shift using RANSAC .... '; sys.stdout.flush()
        shift = stitch.RANSAC(matched_pairs, shifts[-1])
        shifts += shift
        print ' | | best shift ', shift

    print shifts
    '''
    print 'Stitching image .... '; sys.stdout.flush()
    stitched_image = stitch.stitching(shift, image_set_size, height, width)
    print ' | Saved as final.jpg'; sys.stdout.flush()

    print 'Perform end to end alignment'; sys.stdout.flush()
    aligned = stitch.end2end_align(stitched_image, shifts)
    cv2.imwrite('aligned.jpg', aligned)

    print 'Cropping image'; sys.stdout.flush()
    cropped = stitch.crop(aligned)
    cv2.imwrite('cropped.jpg', cropped)
    '''

#plt.show()
