import warpToCylinder as wtc
import sys
import numpy as np
import matplotlib.pyplot as plt

if __name__ == '__main__':
    image_dir = sys.argv[1]
    image_set = wtc.load_images(image_dir)
    focal_length = wtc.load_focal_length(image_dir)
    print (image_set.shape, focal_length.shape)
    cylinder_projs = wtc.cylindrical_projection(image_set, focal_length)
    for cylinder_proj in cylinder_projs:
        cylinder_proj_rgb = cylinder_proj[:,:,::-1]
        plt.imshow(cylinder_proj_rgb)
        plt.show()
