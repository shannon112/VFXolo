import cv2
import numpy as np

#    sift_threshold = 5   sift_cutoff = 0.0003     matched_y_abs_thres = 20
shift_list = [[0,0],[-138,4],[-127, 2],[-98,2], [-69,6],[-103,-8],[-106, 2],
            [-154,-9],[-98,3],[-102,2],[-136, 2],[-134, 4],[-83,3],[-107,-6]]
shift_set = np.array(shift_list)
height = 450
width = 300
image_set_size = 14
img_list = []
for i in range(image_set_size):
    img = cv2.imread(str(i)+'.jpg') # size = 450x300
    img_list.append(img)

#######################################################

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
print new_img.shape # (481,1723,3)
new_h, new_w  = new_img.shape[:2]

'''
# simple stitching by overlap new image on old image
for i,new_i in enumerate(range(0,img1_h)):
    for j,new_j in enumerate(range(0,138)):
        new_img[new_i][new_j] = img1[i][j]
for i,new_i in enumerate(range(4,new_h)):
    for j,new_j in enumerate(range(138,138+img2_w)):
        new_img[new_i][new_j] = img2[i][j]
'''
'''
# linear filter blending at hole overlap area
for i,new_i in enumerate(range(0,img1_h)):
    for j,new_j in enumerate(range(0,138)):
        new_img[new_i][new_j] = img1[i][j]
    for j,new_j in enumerate(range(138,img1_w)):
        new_img[new_i][new_j] += (((img1_w-j-138)/(img1_w-138.))* img1[i][j+138]).astype(np.uint8)
        #print new_img[new_i][new_j]
for i,new_i in enumerate(range(4,new_h)):
    for j,new_j in enumerate(range(138,img1_w)):
        new_img[new_i][new_j] += ((j/(img1_w-138.))*img2[i][j]).astype(np.uint8)
        #print new_img[new_i][new_j]
    for j,new_j in enumerate(range(img1_w,new_w)):
        new_img[new_i][new_j] = img2[i][j+img1_w-138]
'''
'''
# linear filter blending at fixed width boundoury overlap area
br_x = (img1_w+138)/2
bl_r = 15 #fixed_bl_region radius
for i,new_i in enumerate(range(0,img1_h)):
    for j,new_j in enumerate(range(0,br_x-bl_r)):
        new_img[new_i][new_j] = img1[i][j]
    for j,new_j in enumerate(range(br_x-bl_r,br_x+bl_r)):
        new_img[new_i][new_j] += (((2*bl_r-j)/float(2*bl_r)) * img1[i][j+br_x-bl_r]).astype(np.uint8)
for i,new_i in enumerate(range(4,new_h)):
    for j,new_j in enumerate(range(br_x-bl_r,br_x+bl_r)):
        new_img[new_i][new_j] += ((j/float(2*bl_r)) * img2[i][j+br_x-bl_r-138]).astype(np.uint8)
    for j,new_j in enumerate(range(br_x+bl_r,new_w)):
        print j,new_j
        new_img[new_i][new_j] = img2[i][j+br_x+bl_r-138]
'''

left_br_x, right_br_x = 0, 0  #boundoury
for img_num,img in enumerate(img_list):
    bl_r = 15 #fixed_bl_region radius, #blending_r
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

cv2.imwrite('Translation.png', new_img)
