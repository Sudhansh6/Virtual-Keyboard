import cv2
import numpy as np

def click_event(event, x, y, flags, param):
	if cv2.EVENT_LBUTTONDOWN == event:
		# print(x,y)
		font = cv2.FONT_HERSHEY_SIMPLEX
		i = img.copy()
		cv2.putText(i,str(x)+', '+str(y),(x,y),font,1,(0,255,255),2,cv2.LINE_AA)
		cv2.imshow('pic',i)
		b = i[y,x,0] ## NOTICE THIS !!
		g = i[y,x,1]
		r = i[y,x,2]
		wi = np.zeros([100,100,3],np.uint8)
		wi[:]= (b,g,r)
		cv2.imshow('color',wi)
		if cv2.waitKey(0) == ord('q'):
			cv2.destroyWindow('color')

img = cv2.imread('pic.jpg')
cv2.imshow('pic',img)
h,w = img.shape[:2]
print(h,w)
cv2.setMouseCallback('pic',click_event)
if cv2.waitKey(0) == ord('q'):
	cv2.destroyAllWindows()