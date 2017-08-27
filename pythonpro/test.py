import cv2
import numpy as np
import getopt


def salt(img, n):
    for k in range(n):
        i = int(np.random.random() * img.shape[1]);
        j = int(np.random.random() * img.shape[0]);
        if img.ndim == 2:
            img[j, i] = 255
        elif img.ndim == 3:
            img[j, i, 0] = 255
            img[j, i, 1] = 255
            img[j, i, 2] = 255
    return img


if __name__ == '__main__':
    img = cv2.imread("/Users/abc/Desktop/15007.png")
    b, g, r = cv2.split(img)
    merged = cv2.merge([b, g, r])
    cv2.imshow("Merged", merged)
    # cv2.imshow("Blue", b)
    # cv2.imshow("Red", r)
    # cv2.imshow("Green", g)
    cv2.waitKey(0)
    cv2.destroyAllWindows()