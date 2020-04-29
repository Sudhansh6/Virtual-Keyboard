import cv2
import numpy as np
image = cv2.resize(cv2.imread('A.jpeg'),(480,360)) # here it will be h,w

cv2.imshow('1',image)


# cv2.erode(src, kernel[, dst[, anchor[, iterations[, borderType[, borderValue]]]]])
# kernel = np.ones((3,30))
# cv2.imshow('eroded',cv2.erode(image, kernel))
# dilate similar to erode

# cv2.imshow('Gaussian',cv2.GaussianBlur(image, (7, 7),200))# last arg might be std dev
# (10,10) might be the disturbance noise matrix size

# cv2.imshow('Median',cv2.medianBlur(image, 5))
# cv2.imshow('bilateralFilter',cv2.bilateralFilter(image, 9, 75, 75))

# cv2.imshow('bordered',cv2.copyMakeBorder(image, 10, 10, 10, 10, cv2.BORDER_CONSTANT,None,[255,255,0]))
# cv2.BORDER_REFLECT

#cv2.imshow('grayscale',cv2.cvtColor(image, cv2.COLOR_BGR2GRAY))

# M = np.float32([[1, 0, 100], [0, 1, 50]]) 
# (rows, cols) = image.shape[:2] 
# cv2.imshow('translate',cv2.warpAffine(image, M, (cols, rows)))

# cv2.imshow('edge_detection',cv2.Canny(image, 0, 20)) # 20 is sensitivity...lower more sensitive

k = cv2.waitKey(0) & 0XFF
if (k==27):
	cv2.destroyAllWindows()