import cv2

img1 = cv2.imread('1.png')
img2 = cv2.imread('2.png')
cv2.imshow('1',img1)
cv2.imshow('2',img2)

# mask is an 8 bit array adding a mask ig

cv2.imshow('and',cv2.bitwise_and(img1,img2,mask= None))
cv2.imshow('or',cv2.bitwise_or(img1,img2,mask= None))
cv2.imshow('xor',cv2.bitwise_xor(img1,img2,mask= None))
cv2.imshow('not',cv2.bitwise_not(img1))

k = cv2.waitKey(0) and 0XFF
if (k==27):
	cv2.destroyAllWindows()