"""
End to end alignment

Args:
    img: panoramas image
    shifts: all shifts for each image in panoramas

Returns:
    A image that fixed the y-asix shift error
"""
def end2end_align(img, shifts):
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
