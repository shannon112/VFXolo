"""
All constants in this project
Could be adjusted to get a better performance
"""
# siftdetector.py sift threshold
SIFT_THRESHOLD        = 5

# siftmatch.py sift feature matching cutoff
SIFT_MATCH_CUTOFF     = 0.5 #BF  0.0003 #flann
Matched_x_thres_partition = 5 # if == inf means no threshold
Matched_y_thres_partition = 20 # if == 1 means no threshold

# findshift.py def RANSAC(matched_pairs):
RANSAC_K              = 1000 #threshold loop times
RANSAC_THRES_DISTANCE = 3

# stitch.property
OVERLAP_REGION_RADIUS = 25

# crop.py max_black_pixel_num_thres  = final_image_width / denominator
CROP_DENOMINATOR = 50

# main.py applying end to end alignment or not
# if your panoramas is not gradually shift up or down, it's not suggested to use this
ALIGN = True
# main.py applying cropping or not
CROP = True
