import cv2
import sys


def getImgCordinate(filepath, screnFilePath, flag):
	img1 = cv2.imread(filepath)
	img2 = cv2.imread(screnFilePath)

	detector = cv2.AKAZE_create()
	norm = cv2.NORM_HAMMING
	matcher = cv2.BFMatcher(norm)

	if img1 is None:
		print('Failed to load fn1:', fn1)
		sys.exit(1)

	if img2 is None:
		print('Failed to load fn2:', fn2)
		sys.exit(1)

	if detector is None:
		print('unknow feature:', feature_name)
		sys.exit(1)

	print('using akaze')

    kp1, desc1 = detector.detectAndCompute(img1, None)
    kp2, desc2 = detector.detectAndCompute(img2, None)
    print('matchin...')
    raw_matchs = matcher.knnMatch(desc1, trainDescriptors = desc2, k=2)
    p1, p2, kp_paris = filter_matchs(kp1, kp2, raw_matchs)

    raw_input("enter")
    if len(p1) >=4:
        H, status = cv2.findHomography(p1, p2, cv2.RANSAC, 5.0)
        print('%d / %d inliers/matched' % (np.sum(status), len(status)))
    else:
        print('匹配失败')

    h1, w1 = img1.shape[:2]
    h2, w2 = img2.shape[:2]
    obj_corners = np.float32([[0, 0], [w1, 0], [w1, h1], [0, h1]])
    obj_corners = obj_corners.reshape(-1, 2)
    img3 = cv2.rectangle(img2, (int(round(scene_corners[3][0])),int(round(scene_corner[3][1])),int(round(scene_corner[1][0])),int(round(scene_corner[1][1]))), (0,255,0), 3)
    resultpath = os.path.join(r'', flag + '_match.png')
    cv2.imwrite(resultpath, img3)
    mid_cordinate_x = int(round((scene_corners[3][0] + scene_corners[1][0])/2))
    mid_cordinate_y = int(round((scene_corners[3][1] + scene_corners[1][1])/2))
    return mid_cordinate_x, mid_cordinate_y