import cv2
import numpy as np 

def nothing(x) : pass

cap = cv2.VideoCapture(0) # Start Livefeed

cv2.waitKey(3000) # Wait for three seconds and take background picture
_,pic = cap.read()
pic = cv2.cvtColor(pic,cv2.COLOR_BGR2HSV) # Convert into HSV Colorspace

cv2.namedWindow('frame')

try:
	f = open('hsv_values.txt','r') # check if hsv values are present
	a = list(int(x.replace('\n','')) for x in f)
	h,s,v,H,S,V = a
	f.close()
except:
	H,S,V,h,s,v = 0,0,0,0,0,0
	pass
		

cv2.createTrackbar('h_low','frame',h,180,nothing)
cv2.createTrackbar('s_low','frame',s,255,nothing)
cv2.createTrackbar('v_low','frame',v,255,nothing)

cv2.createTrackbar('h_high','frame',H,180,nothing) # create trackbars for h,s,v values
cv2.createTrackbar('s_high','frame',S,255,nothing)
cv2.createTrackbar('v_high','frame',V,255,nothing)

while(cap.isOpened()):

	ret,frame = cap.read() # Start taking input from camera
	frame = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV) 
	H = cv2.getTrackbarPos('h_high','frame') # take h,s,v low and high inputs to match the cloak's colors
	S = cv2.getTrackbarPos('s_high','frame')
	V = cv2.getTrackbarPos('v_high','frame')
	h = cv2.getTrackbarPos('h_low','frame')
	s = cv2.getTrackbarPos('s_low','frame')
	v = cv2.getTrackbarPos('v_low','frame')

	low = np.array([h,s,v]) 
	high = np.array([H,S,V]) 
	
	mask = cv2.inRange(frame,low,high) # Create a mask with low and high filters
	arr = np.where(mask!=0) # index of pixels where cloak is present
	frame[arr] = pic[arr] # Replace the cloak with background
	frame = cv2.cvtColor(frame,cv2.COLOR_HSV2BGR) # convert back to bgr to display

	cv2.imshow('frame',frame)
	cv2.imshow('mask',mask)

	k = cv2.waitKey(50) & 0XFF
	if(k == ord('q')): 
		break
f = open('hsv_values.txt','w+')
 # store the values in a file
f.write(str(h)+'\n'+str(s)+'\n'+str(v)+'\n')
f.write(str(H)+'\n'+str(S)+'\n'+str(V)+'\n')
f.close()

cap.release()
cv2.destroyAllWindows() 
