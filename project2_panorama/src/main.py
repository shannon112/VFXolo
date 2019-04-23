import warpToCylinder as wtc
import sys
import numpy as np
import math
import matplotlib.pyplot as plt

if __name__ == '__main__':
    image_dir = sys.argv[1]
    image_set = wtc.load_images(image_dir)
    focal_length = wtc.load_focal_length(image_dir)
    print ("image_set",image_set.shape, "focal_length set",focal_length.shape)

    cylinder_projs = wtc.cylindrical_projection(image_set, focal_length)
    fig1=plt.figure().suptitle('cylindrical_projection')
    for i,cylinder_proj in enumerate(cylinder_projs):
        cylinder_proj_rgb = cylinder_proj[:,:,::-1]
        subfig = plt.subplot("2"+str(math.ceil(image_set.shape[0]/2))+str(i+1))
        subfig.imshow(cylinder_proj_rgb)
plt.show()
