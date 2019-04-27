import cv2
import numpy as np
import sys
import constant as const


"""
Crop the absolute black(0) border in pano image

Args:
    img: a panoramas image array

Returns:
    cropped image array
"""
def crop(img):
    #if absolutely black then consider as the region need to crop
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, img_thresh = cv2.threshold(img_gray, 0, 255, cv2.THRESH_BINARY)

    upper_y, lower_y = [0, img.shape[0]]
    max_black_pixel_num_thres = img.shape[1]//const.CROP_DENOMINATOR

    #from up to down, break at if there have enough info pixel
    for y in range(img_thresh.shape[0]):
        if len(np.where(img_thresh[y] == 0)[0]) < max_black_pixel_num_thres:
            upper_y = y
            break

    #bottom up, break at if there have enough info pixel
    for y in range(img_thresh.shape[0]-1, 0, -1):
        if len(np.where(img_thresh[y] == 0)[0]) < max_black_pixel_num_thres:
            lower_y = y
            break

    return img[upper_y:lower_y, :]

if __name__ == '__main__':
    image_fn = sys.argv[1]
    img = cv2.imread(image_fn)
    img = crop(img)
    cv2.imwrite('cropped_'+image_fn,img)
