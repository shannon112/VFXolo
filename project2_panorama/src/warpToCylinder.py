# coding: utf-8
import os
import sys
import cv2
import math
import glob
import numpy as np
import matplotlib.pyplot as plt


def load_images(source_dir):
    img_filenames = sorted(glob.glob(os.path.join(source_dir, '*.jpg'))) # would be one of jpg or JPG
    #img_filenames = sorted(glob.glob(os.path.join(source_dir, '*.JPG'))) # would be one of jpg or JPG
    image_list = [cv2.imread(img_filename, 1) for img_filename in img_filenames]
    return np.array(image_list)

def load_focal_length(source_dir):
    info_filename = glob.glob(os.path.join(source_dir, 'info.txt'))
    focal_length = []
    f = open(info_filename[0])
    for line in f:
        if (line[0] == '#'): continue
        (image_name, image_focal_length) = line.strip().split(" ")
        focal_length.append(float(image_focal_length))
    return np.array(focal_length)


def cylindrical_projection(imgs, focal_lengths):
    num, height, width, _ = imgs.shape
    cylinder_projs = []
    for i,img in enumerate(imgs):
        cylinder_proj = np.zeros(shape=img.shape, dtype=np.uint8)
        focal_length = focal_lengths[i]
        for y in range(-int(height/2), int(height/2)):
            for x in range(-int(width/2), int(width/2)):
                cylinder_x = focal_length*math.atan(x/focal_length)
                cylinder_y = focal_length*y/math.sqrt(x**2+focal_length**2)

                cylinder_x = int(round(cylinder_x + width/2))
                cylinder_y = int(round(cylinder_y + height/2))
                if cylinder_x >= 0 and cylinder_x < width and cylinder_y >= 0 and cylinder_y < height:
                    cylinder_proj[cylinder_y][cylinder_x] = img[y+int(height/2)][x+int(width/2)]
        print ("project image {} to cylinderical coordinate...".format(i))
        # Crop black border
        # ref: http://stackoverflow.com/questions/13538748/crop-black-edges-with-opencv
        #gray = cv2.cvtColor(cylinder_proj,cv2.COLOR_BGR2GRAY)
        #_,thresh = cv2.threshold(gray,1,255,cv2.THRESH_BINARY)
        #contours,hierarchy = cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        #cnt = contours[0]
        #x,y,w,h = cv2.boundingRect(cnt)
        cylinder_projs.append(cylinder_proj)#[y:y+h, x:x+w])

    return cylinder_projs


if __name__ == '__main__':
    image_dir = sys.argv[1]
    image_set = load_images(image_dir)
    focal_length = load_focal_length(image_dir)
    print (image_set.shape, focal_length.shape)
    cylinder_projs = cylindrical_projection(image_set, focal_length)
    for cylinder_proj in cylinder_projs:
        cylinder_proj_rgb = cylinder_proj[:,:,::-1]
        plt.imshow(cylinder_proj_rgb)
        plt.show()
