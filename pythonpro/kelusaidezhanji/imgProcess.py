#!/usr/bin/python3
# -*- coding:utf-8 -*-


import sys
import getopt
import cv2
from cv2 import *

def getImgCordinate(filepath, screenfilepath, flag=0):
    img1 = cv2.imread(filepath)
    img2 = cv2.imread(screenfilepath)
    img1.
    detector = cv2.AKAZE_create()
    norm = cv2.NORM_HAMMING
    matcher = cv2.BFMatcher(norm)

    if img1 is None:
        print('Failed to load ')
        sys.exit(1)

    if img2 is None:
        print('Falied to load img2')
        sys.exit(1)

    if detector is None:
        print('unknow')
        sys.exit(1)

    print('using akaze')
    kp1, desc1 = detector.detectAndCompute(img1, None)
    kp2, desc2 = detector.detectAndCompute(img2, None)
    print(kp1, kp2)

    print('matching')
    raw_matches = matcher.knnMatch(desc1, trainDescriptors=desc2, k=2)
    print(raw_matches)
    p1 , p2 ,kp_pairs = filter_matches(kp1, kp2, raw_matches)


if __name__ == '__main__':
    getImgCordinate('/Users/runehero/Desktop/yang.png', '/Users/runehero/Desktop/apk_test.png')
