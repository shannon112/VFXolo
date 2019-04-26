# coding: utf-8
import matplotlib.pyplot as plt
import numpy as np
import cv2
import constant as const
from PIL import ImageTk, Image

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
def RANSAC(matched_pairs):
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

    return list(best_shift)


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
def stitching_wo_blending(shift_list, image_set_size, height, width):
    # shift_list w/o initail [0,0]
    img_list = []
    for i in range(image_set_size):
        img = Image.open(str(i)+'.jpg') # size = 450x300
        img_list.append(img)
    shift_set = np.array(shift_list)

    shift_x = 0 #-1423
    shift_y = 0
    shift_y_max = -1*float("inf") #30
    shift_y_min = float("inf") #-1
    for shift in shift_list:
        shift_x += shift[0]
        shift_y += shift[1]
        if shift_y<shift_y_min: shift_y_min=shift_y
        if shift_y>shift_y_max: shift_y_max=shift_y

    new_size = (width+abs(shift_x),height+abs(shift_y_min)+abs(shift_y_max)) # w,h
    new_im = Image.new("RGBA", new_size) # makes the black image

    for i,img in enumerate(img_list):
        shift_sum = np.array([0,0])
        for shift in shift_set[:i]: shift_sum+=shift
        shift_x_accumulation,_ = shift_sum
        shift_sum = np.array([0,0])
        for shift in shift_set[:len(img_list)-i]: shift_sum+=shift
        _,shift_y_accumulation = shift_sum
        new_im.paste(img, (abs(shift_x_accumulation),abs(shift_y_min)+shift_y_accumulation))
    new_im.show()
    new_im.save('final.jpg')
    return 0


def stitching_w_blending(shift_list, image_set_size, height, width):
    # shift_list w/ initail [0,0]
    shift_set = np.array(shift_list)
    img_list = []
    for i in range(image_set_size):
        img = cv2.imread(str(i)+'.jpg') # size = 450x300
        img_list.append(img)

    shift_x = 0 #-1423
    shift_y = 0
    shift_y_max = -1*float("inf") #30
    shift_y_min = float("inf") #-1
    for shift in shift_list:
        shift_x += shift[0]
        shift_y += shift[1]
        if shift_y<shift_y_min: shift_y_min=shift_y
        if shift_y>shift_y_max: shift_y_max=shift_y

    # calculate left-top point coordinate of each image coming in pano scale
    # camera from left turn right
    # shift would be x,y    x<0  y not sure
    # pano coordinate go down go right is positive
    shift_acc=[] #shift_accumulations
    shift_sum = np.array([0,0])
    for shift in shift_set:
        shift_sum+=shift
        temp = shift_sum.copy()
        temp[0] = -1*temp[0]
        shift_acc.append(temp)
    print shift_acc, len(shift_acc)

    new_img = np.zeros( (height+abs(shift_y_min)+abs(shift_y_max), width+abs(shift_x),3),dtype=np.uint8)
    new_h, new_w  = new_img.shape[:2]
    print new_img.shape # (481,1723,3)

    left_br_x, right_br_x = 0, 0  #boundoury
    for img_num,img in enumerate(img_list):
        bl_r = const.OVERLAP_REGION_RADIUS #fixed_bl_region radius, #blending_r
        for i,new_i in enumerate(range(shift_acc[img_num][1]+abs(shift_y_min), height+shift_acc[img_num][1]+abs(shift_y_min))):
            if img_num == 0: #shape |-\
                left_br_x = 0
                right_br_x = ((shift_acc[img_num][0]+width) + shift_acc[img_num+1][0])/2
                for j,new_j in enumerate(range(0, right_br_x-bl_r)): # flatten, uniform
                    new_img[new_i][new_j] = img[i][j]
                for j,new_j in enumerate(range(right_br_x-bl_r, right_br_x+bl_r)):  # linear decreasing
                    new_img[new_i][new_j] += (((2*bl_r-j)/float(2*bl_r)) * img[i][j + right_br_x - bl_r]).astype(np.uint8)

            elif img_num == image_set_size-1: #shape /-|
                right_br_x = new_w
                for j,new_j in enumerate(range(left_br_x-bl_r, left_br_x+bl_r)): # linear increasing
                    new_img[new_i][new_j] += ((j/float(2*bl_r)) * img[i][ j + (left_br_x-bl_r) - shift_acc[img_num][0]]).astype(np.uint8)
                for j,new_j in enumerate(range(left_br_x+bl_r, new_w)): # flatten, uniform
                    new_img[new_i][new_j] = img[i][ j + (left_br_x+bl_r) - shift_acc[img_num][0]]

            else: #shape /-\
                right_br_x = ((shift_acc[img_num][0]+width) + shift_acc[img_num+1][0])/2
                for j,new_j in enumerate(range(left_br_x-bl_r, left_br_x+bl_r)): # linear increasing
                    new_img[new_i][new_j] += ((j/float(2*bl_r)) * img[i][ j + (left_br_x-bl_r) - shift_acc[img_num][0]]).astype(np.uint8)
                for j,new_j in enumerate(range(left_br_x+bl_r, right_br_x-bl_r)): # flatten, uniform
                    new_img[new_i][new_j] = img[i][ j + (left_br_x+bl_r) - shift_acc[img_num][0]]
                for j,new_j in enumerate(range(right_br_x-bl_r, right_br_x+bl_r)):  # linear decreasing
                    new_img[new_i][new_j] += (((2*bl_r-j)/float(2*bl_r)) * img[i][j + (right_br_x-bl_r) - shift_acc[img_num][0]]).astype(np.uint8)
        left_br_x = right_br_x
    cv2.imwrite('translation.jpg', new_img)
    return 0
