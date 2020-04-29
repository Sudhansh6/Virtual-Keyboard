import cv2 
import numpy as np
import datetime

# a = np.array([1,2,3])
# b = np.array([4,5,6])
# c = np.array(zip(a,b))
# print(c)
# c = np.resize(c,(2,3))
# print(c)

img = cv2.resize(cv2.imread('pic.jpg'),(720,480))
video = cv2.VideoCapture(-1) 
Color = np.array(cv2.split(img))
h,w  = img.shape[:2]
# video.set(3,1280)
# video.set(4,960)
# print(video.get(3),video.get(4))

while(True):

	ret,frame = video.read()
	frame = cv2.resize(frame,(w,h))

	color = np.array(cv2.split(frame))
	b = np.logical_and(100<=color[0],color[0]<=255)
	g = np.logical_and(120<=color[1],color[1]<=255)
	r = np.logical_and(120<=color[2],color[2]<=255)

	index1 = np.where(b,1,0)
	index2 = np.where(g,1,0)
	index3 = np.where(r,1,0)
	index = index1 + index2 + index3
	color = np.where(index==3)
	#frame[color] = img [color]
	font = cv2.FONT_HERSHEY_SIMPLEX
	frame = cv2.putText(frame,str(datetime.datetime.now()),(0,100),font,
		1,(0,255,0),2,cv2.LINE_AA)
	cv2.imshow('frame',frame)

	if cv2.waitKey(10) & 0XFF == ord('q'):
		break

video.release()
cv2.destroyAllWindows() 
