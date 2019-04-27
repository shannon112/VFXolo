import sys
import numpy as np
import cv2


"""
End to end alignment

Args:
    img: panoramas image array
    shifts: all shifts for each image in panoramas

Returns:
    Aligned image array
"""
def e2eAlign(img, shifts):
    height, width = img.shape[:2]
    shifts_set = np.array(shifts)
    total_shift_x, total_shift_y = np.sum(shifts, axis=0)

    scatter_shift = None

    # shift inverse position
    if total_shift_y < 0:
        scatter_shift = np.linspace(0,-1*total_shift_y , num=width, dtype=np.uint8)
    elif total_shift_y > 0:
        scatter_shift = np.linspace(0,-1*total_shift_y , num=width, dtype=np.uint8)
    print scatter_shift.shape, img.shape

    img_aligned = img.copy()
    for x in range(width):
        img_aligned[:,x] = np.roll(img[:,x], scatter_shift[x], axis=0)

    return img_aligned

if __name__ == '__main__':
    image_fn = sys.argv[1]
    img = cv2.imread(image_fn)
    shifts = [[0, 0], [-253, -3], [-242, -4], [-246, -4], [-248, -4], [-241, -5], [-247, -5], [-250, -4], [-241, -5], [-247, -4],
                [-248, -4], [-242, -4], [-252, -5], [-242, -3], [-249, -5], [-242, -5], [-245, -4], [-246, -4]]
    img = e2eAlign(img,shifts)
    cv2.imwrite('aligned_'+image_fn,img)
