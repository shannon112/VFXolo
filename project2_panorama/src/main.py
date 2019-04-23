import warpToCylinder as wtc
import sys
import numpy as np
import math
import matplotlib.pyplot as plt

if __name__ == '__main__':
    # read files
    image_dir = sys.argv[1]
    image_set = wtc.load_images(image_dir)
    focal_length = wtc.load_focal_length(image_dir)
    image_set_size, height, width, _ =  image_set.shape
    print ('image_set',image_set.shape, 'focal_length set',focal_length.shape)

    # project to cylinder coordinate
    cylinder_projs = wtc.cylindrical_projection(image_set, focal_length)
    fig1=plt.figure().suptitle('cylindrical_projection')
    for i,cylinder_proj in enumerate(cylinder_projs):
        cylinder_proj_rgb = cylinder_proj[:,:,::-1]
        subfig = plt.subplot(2,math.ceil(image_set_size/2),i+1)
        subfig.imshow(cylinder_proj_rgb)

    # initail values
    stitched_image = cylinder_projs[0].copy()
    shifts = [[0, 0]]
    feature_cache = [[], []]


    for i in range(1, image_set_size):
        print('Computing ...... {}/{}'.format(str(i),str(image_set_size-1)))
        img1 = cylinder_projs[i-1]
        img2 = cylinder_projs[i]

        print(' | Reload features in previous image .... ')
        descriptions1, position1 = feature_cache
        if i==1: #first loop
            raw_features1 = feature.sift_detector(img1)
            descriptions1, position1 = feature.sift_descriptor(img1, raw_features1)
        print(' | | {} features are extracted'.formate(str(len(descriptions1))))


        print(' | Find features in image #{} ... '.format(str(i+1)))
        raw_features2 = feature.sift_detector(img2)
        descriptors2, position2 = feature.sift_descriptor(img2, raw_features2)
        feature_cache = [descriptors2, position2]
        print(' | | {} features are extracted'.formate(str(len(descriptions2))))


        '''
        if const.DEBUG:
            cv2.imshow('cr1', corner_response1)
            cv2.imshow('cr2', corner_response2)
            cv2.waitKey(0)

        print(' - Feature matching .... ', end='', flush=True)
        matched_pairs = feature.matching(descriptions1, descriptors2, position1, position2, pool, y_range=const.MATCHING_Y_RANGE)
        print(str(len(matched_pairs)) +' features matched.')

        if const.DEBUG:
            utils.matched_pairs_plot(img1, img2, matched_pairs)

        print(' - Find best shift using RANSAC .... ', end='', flush=True)
        shift = stitch.RANSAC(matched_pairs, shifts[-1])
        shifts += [shift]
        print('best shift ', shift)

        print(' - Stitching image .... ', end='', flush=True)
        stitched_image = stitch.stitching(stitched_image, img2, shift, pool, blending=True)
        cv2.imwrite(str(i) +'.jpg', stitched_image)
        print('Saved.')


    print('Perform end to end alignment')
    aligned = stitch.end2end_align(stitched_image, shifts)
    cv2.imwrite('aligned.jpg', aligned)

    print('Cropping image')
    cropped = stitch.crop(aligned)
    cv2.imwrite('cropped.jpg', cropped)
    '''
plt.show()
