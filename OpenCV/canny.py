import cv2

def nothing(x): pass

img = cv2.resize(cv2.imread('1.jpeg'),(480,360))

cv2.namedWindow('img')
cv2.createTrackbar('2','img',0,300,nothing)
cv2.createTrackbar('3','img',0,300,nothing)
cv2.createTrackbar('4','img',1,3,nothing)


while(True):
	b = cv2.getTrackbarPos('2','img')
	c = cv2.getTrackbarPos('3','img')
	d = cv2.getTrackbarPos('4','img')
	
	img2 = cv2.Canny(img, b, c,apertureSize = 2*d+1)
	cv2.imshow('img',img2)

	if cv2.waitKey(100) & 0XFF == ord('q'):
		break
cv2.destroyAllWindows()