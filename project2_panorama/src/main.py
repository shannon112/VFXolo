import sys
import numpy as np
import math
import matplotlib.pyplot as plt
import cv2
import multiprocessing as mp

import warpToCylinder as wtc
from siftdetector import sift_detector
from siftmatch import sift_matching_BT
import stitch
import constant as const
import crop
import alignment

# stiching from left to right
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
    shifts = [[0,0]] #every shift between two nearby images
    feature_cache = [[], []] #store last image feature

    # feature detecting, discriping, matching and shift finding
    for i in range(1, image_set_size):
        print 'Computing ...... {}/{}'.format(str(i),str(image_set_size-1)); sys.stdout.flush()
        img1 = str(i-1)+".jpg"
        img2 = str(i)+".jpg"
        img1_cv = cylinder_projs[i-1].copy()
        img2_cv = cylinder_projs[i].copy()

        print ' | Reload features in previous image .... '; sys.stdout.flush()
        keypints1, descriptors1 = feature_cache
        if i==1: #first loop
            keypints1, descriptors1 = sift_detector(img1)
        print ' | | | {} features are extracted'.format(str(len(descriptors1))); sys.stdout.flush()

        print ' | Find features in image #{} ... '.format(str(i+1)); sys.stdout.flush()
        keypints2, descriptors2 = sift_detector(img2)
        feature_cache = [keypints2, descriptors2]
        print ' | | | {} features are extracted'.format(str(len(descriptors2))); sys.stdout.flush()

        print ' | Feature matching .... '; sys.stdout.flush()
        matched_pairs = sift_matching_BT(img1, img2 , keypints1, descriptors1, keypints2, descriptors2)
        print ' | | ' + str(len(matched_pairs)) + ' features matched.'; sys.stdout.flush()

        print ' | Find best shift using RANSAC .... '; sys.stdout.flush()
        shift = stitch.RANSAC(matched_pairs)
        shifts.append(shift)
        print ' | | best shift ', shift
    print 'Completed feature matching! Here are all shifts:'; sys.stdout.flush()
    print shifts;  sys.stdout.flush()

    # stitching and blending
    print 'Stitching image ... '; sys.stdout.flush()
    stitched_image = stitch.stitching_w_blending(shifts, image_set_size, height, width)
    cv2.imwrite('pano.jpg', stitched_image)
    print ' | Saved as pano.jpg'; sys.stdout.flush()
    pano_image = stitched_image.copy()

    # end to end alignment
    if const.ALIGN:
        print 'End to end alignment ... '; sys.stdout.flush()
        aligned_image = alignment.e2eAlign(pano_image, shifts)
        cv2.imwrite('aligned_pano.jpg', aligned_image)
        print ' | Saved as aligned_pano.jpg'; sys.stdout.flush()
        pano_image = aligned_image.copy()

    # cropping
    if const.CROP:
        print 'Cropping image ... '; sys.stdout.flush()
        cropped_image = crop.crop(pano_image)
        cv2.imwrite('cropped_pano.jpg', cropped_image)
        print ' | Saved as cropped_pano.jpg'; sys.stdout.flush()
        pano_image = cropped_image.copy()
#plt.show()
