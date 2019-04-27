import matplotlib.pyplot as plt
import numpy as np
import cv2
import constant as const
from PIL import ImageTk, Image


"""
Find best shift using RANSAC

Args:
    matched_pairs: matched pairs of feature's positions,
                    its an Nx2x2 matrix
                    (N pairs, (oldImg_x,oldImg_y), (newImg_x,newImg_y))

Returns:
    Best shift [x,y] as a 1x2 list
"""
def RANSAC(matched_pairs):
    matched_pairs = np.asarray(matched_pairs)
    use_random = True if len(matched_pairs) > const.RANSAC_K else False
    K = const.RANSAC_K if use_random else len(matched_pairs)
    threshold_distance = const.RANSAC_THRES_DISTANCE

    best_shift = []
    max_inliner = 0
    for k in range(K):
        # Random pick a pair of matched feature
        idx = int(np.random.random_sample()*len(matched_pairs)) if use_random else k
        sample = matched_pairs[idx] # pick one pair of matching features

        # calculate shift
        shift = sample[1] - sample[0] # next one - last one

        # calculate inliner points
        predicted_pt = matched_pairs[:,1] - shift  # next one - shift = predicted last one
        differences = matched_pairs[:,0] - predicted_pt # last one - predicted last one
        inliner = 0
        for diff in differences:
            if np.sqrt((diff**2).sum()) < threshold_distance: # 2-norm distance
                inliner = inliner + 1
        if inliner > max_inliner:
            max_inliner,best_shift = inliner,shift

    return list(best_shift)
