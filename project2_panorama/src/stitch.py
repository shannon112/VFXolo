# coding: utf-8
import matplotlib.pyplot as plt
import numpy as np
import cv2
import constant as const
import multiprocessing as mp

"""
Find best shift using RANSAC

Args:
    matched_pairs: matched pairs of feature's positions, its an Nx2x2 matrix
    prev_shift: previous shift, for checking shift direction.

Returns:
    Best shift [y x]. ex. [4 234]

Raise:
    ValueError: Shift direction NOT same as previous shift.
"""
def RANSAC(matched_pairs, prev_shift):
    matched_pairs = np.asarray(matched_pairs)
    use_random = True if len(matched_pairs) > const.RANSAC_K else False

    best_shift = []
    K = const.RANSAC_K if use_random else len(matched_pairs)
    threshold_distance = const.RANSAC_THRES_DISTANCE

    max_inliner = 0
    for k in range(K):
        # Random pick a pair of matched feature
        idx = int(np.random.random_sample()*len(matched_pairs)) if use_random else k
        sample = matched_pairs[idx] # pick one pair of matching features

        # fit the warp model
        shift = sample[1] - sample[0]

        # calculate inliner points
        shifted = matched_pairs[:,1] - shift
        difference = matched_pairs[:,0] - shifted

        inliner = 0
        for diff in difference:
            if np.sqrt((diff**2).sum()) < threshold_distance:
                inliner = inliner + 1

        if inliner > max_inliner:
            max_inliner = inliner
            best_shift = shift
    '''
    if prev_shift[1]*best_shift[1] < 0:
        print('\n\nBest shift:', best_shift)
        raise ValueError('Shift direction NOT same as previous shift.')
    '''
    return best_shift


"""
Stitch two image with blending.

Args:
    img1: first image
    img2: second image
    shift: the relative position between img1 and img2
    blending: using blending or not

Returns:
    A stitched image
"""
#def stitching(img1, img2, shift, blending=True):
