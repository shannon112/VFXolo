#!/usr/bin/python -tt
# | | best shift  [-138,4]
# | | best shift  [-127, 2]
# | | best shift  [-98,2]
# | | best shift  [-69,6]
# | | best shift  [-103,-8] wired more x
# | | best shift  [-106, 2]
# | | best shift  [-154,-9] wired less x
# | | best shift  [-98,3] wired more y
# | | best shift  [-68,19]
# | | best shift  [-136, 2]
# | | best shift  [-134, 4]
# | | best shift  [-83,3]
# | | best shift  [-109,-7]


from PIL import ImageTk, Image
import numpy as np

#    sift_threshold = 5   sift_cutoff = 0.0003     matched_y_abs_thres = 45
#shift_list = [[-138,4],[-127, 2],[-98,2], [-69,6],[-103,-8],[-106, 2],
#            [-154,-9],[-98,3],[-68,19],[-136, 2],[-134, 4],[-83,3],[-109,-7]]

#    sift_threshold = 5   sift_cutoff = 0.0001    matched_y_abs_thres = 45
#shift_list = [[-137,6],[-126, 1],[-98,2], [-104,11],[-103,-8],[-106, 2],
#            [-63,13],[-98,3],[-91,44],[-136, 2],[-152, 1],[-72,2],[-98,6]]

#    sift_threshold = 5   sift_cutoff = 0.0003     matched_y_abs_thres = 20
shift_list = [[-138,4],[-127, 2],[-98,2], [-69,6],[-103,-8],[-106, 2],
            [-154,-9],[-98,3],[-102,2],[-136, 2],[-134, 4],[-83,3],[-107,-6]]


img_list = []
for i in range(13):
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

new_size = (300+abs(shift_x),450+abs(shift_y_min)+abs(shift_y_max)) # w,h
new_im = Image.new("RGBA", new_size) # makes the black image

for i,img in enumerate(img_list):
    shift_sum = np.array([0,0])
    for shift in shift_set[:i]: shift_sum+=shift
    shift_x_accumulation,_ = shift_sum
    shift_sum = np.array([0,0])
    for shift in shift_set[:len(img_list)-i]: shift_sum+=shift
    _,shift_y_accumulation = shift_sum
    new_im.paste(img, (abs(shift_x_accumulation),abs(shift_y_min)+shift_y_accumulation))
    print abs(shift_x_accumulation) , abs(shift_y_min)+shift_y_accumulation

    #new_im.paste(img, (0,4+2+2+6))
    #new_im.paste(old_im2,(138,2+2+6))
    #new_im.paste(old_im3,(138+127,2+6))
    #new_im.paste(old_im4,(138+127+98,6))
    #new_im.paste(old_im5,(138+127+98+69,0))
new_im.show()
new_im.save('final.jpg')
