"""
End to end alignment

Args:
    img: a panoramas image array
    shifts: all shifts for each image in panoramas

Returns:
    Aligned image array
    A image that fixed the y-asix shift error
"""
def e2eAlign(img, shifts):
    shifts = np.array(shifts)
    sum_y, sum_x = np.sum(shifts, axis=0)

    y_shift = np.abs(sum_y)
    col_shift = None

    # same sign
    if sum_x*sum_y > 0:
        col_shift = np.linspace(y_shift, 0, num=img.shape[1], dtype=np.uint16)
    else:
        col_shift = np.linspace(0, y_shift, num=img.shape[1], dtype=np.uint16)

    aligned = img.copy()
    for x in range(img.shape[1]):
        aligned[:,x] = np.roll(img[:,x], col_shift[x], axis=0)

    return aligned

if __name__ == '__main__':
    image_fn = sys.argv[1]
    img = cv2.imread(image_fn)
    shifts = [[0, 0], [-253, -3], [-242, -4], [-246, -4], [-248, -4], [-241, -5], [-247, -5], [-250, -4], [-241, -5], [-247, -4],
                [-248, -4], [-242, -4], [-252, -5], [-242, -3], [-249, -5], [-242, -5], [-245, -4], [-246, -4]]
    img = end2end_align(img,shifts)
    cv2.imwrite('aligned_'+image_fn+'.jpg',img)
