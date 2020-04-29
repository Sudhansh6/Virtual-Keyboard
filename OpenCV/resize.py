import cv2  
  
image1 = cv2.imread('A.jpeg')
w,h = image1.shape[:2]
print(w,h)
image = cv2.resize(cv2.imread('A.jpeg'),(720,540)) # here it will be h,w

cv2.imshow('1',image)
#cv2.imshow('half',cv2.resize(image, (0, 0), fx = 0.1, fy = 0.1) )

im = image[48:398,39:299] # note that her it will be w,h
cv2.imshow('region',im)
cv2.imshow('bigger',cv2.resize(im, (700, 520))) # h,w again
# cv2.imshow('stretch_near' ,cv2.resize(image, (780, 540),interpolation = cv2.INTER_NEAREST))

k = cv2.waitKey(0) & 0XFF
if(k==27):
	cv2.destroyAllWindows()