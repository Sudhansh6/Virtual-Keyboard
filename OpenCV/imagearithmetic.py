import cv2

img1 = cv2.resize(cv2.imread('1.jpeg'),(300,300))
img2 = cv2.resize(cv2.imread('2.jpeg'),(300,300))
cv2.imshow('1',img1)
cv2.imshow('2',img2)

wt1 = 0.7
wt2 = 0.3
gammaValue = 0 # Measurement of light

# Arithmetics require same size and depth of image.
cv2.imshow('add',cv2.add(img1, img2))
cv2.imshow('wadd',cv2.addWeighted(img1, wt1, img2, wt2, gammaValue))
cv2.imshow('subtract',cv2.subtract(img1,img2))

k = cv2.waitKey(0) & 0XFF
if(k==27):
	cv2.destroyAllWindows()