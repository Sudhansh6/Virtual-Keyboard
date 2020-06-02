import cv2
import numpy as np
import pytesseract
import re

cap = cv2.VideoCapture(-2)
count,shift,caps,new_file = 0,False,True,' '
typed = text = old_file =  ''
pts1 = pts2 = title = np.float32([[0,0],[640,0],[640,480],[0,480]])
pts3 = np.float32([[0,0],[450,0],[450,120],[0,120]])
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi',fourcc,20,(640,480))

def crop(thresh,old_pts):
	contours,_ = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
	sorted_contours = sorted(contours, key=lambda x: cv2.contourArea(x),reverse = True)
	cnts,heading = sorted_contours[:2]
	l = list(cv2.approxPolyDP(cnts,0.01*cv2.arcLength(cnts,True),True) for cnts in sorted_contours[:2])
	pts = [0,0]
	for i in range(2):
		if(len(l[i])==4):
			l[i] = l[i].reshape(-1,2)
			c = np.argsort(np.sum(l[i],axis = 1))
			if(l[i][c[1]][0] < l[i][c[2]][0]):
				c[2],c[1] = c[1],c[2]
			c[2],c[3]=c[3],c[2]
			pts[i] = np.float32(l[i][c])
		else:
			pts[i] = old_pts[i]
	return pts

def extract(keyboard,file):
	print("Extracting keys from keyboard")
	location = []
	kcontours,_ = cv2.findContours(keyboard,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
	for cnt in kcontours:
		cnt = cv2.approxPolyDP(cnt, 0.02*cv2.arcLength(cnt, True), True)
		if len(cnt) == 4 and 12000>cv2.contourArea(cnt) and cv2.contourArea(cnt)> 400 and cv2.isContourConvex(cnt):
			a = cnt.reshape(-1, 2)
			c = np.argsort(np.sum(a,axis = 1))
			if(a[c[1]][0] < a[c[2]][0]):
				c[2],c[1] = c[1],c[2]
			c[2],c[3]=c[3],c[2]
			location.append((a[c[0]],a[c[2]]))
	print('Extracted')
	location = sorted(location,key = lambda x: (x[0][1]//40,x[0][0]))
	with open(file+'.txt') as f:
		print(file + ' read.')
		data = f.read().replace('\n', '')

	return (data,np.array(location))


def mask(frame):
	try:
		f = open('hsv_values.txt','r') # check if hsv values are present
		h,s,v,H,S,V = list(int(x.replace('\n','')) for x in f)
		f.close()
	except:
		h,s,v = 108, 61, 23
		H,S,V = 255,180,180

	low,high = np.array([h,s,v]),np.array([H,S,V]) 
	frame = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV) 
	mask = cv2.inRange(frame,low,high) # Create a mask with low and high filters
	opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((7,7),np.int8),10)
	return opening

def display(pressed,text,frame,typed,shift,caps):
	for i in pressed:
		if(text[i]=='←'): 
			typed = typed[:-1]
			x = ''
		elif(text[i]=='↲'):
			x = '\n'
		elif(text[i]=='↑'):
			x =''
			shift = not shift
		elif(caps):
			x = text[i]
		else:
			x = text[i].lower()
		typed += x
		# print(typed ,end = '\r')
	return (typed,shift)

while(True):
	_,frame = cap.read()
	touched,pressed = set(),set()

	if not count:
		h,w = frame.shape[:2]
		touched_1 = set()

	thresh = cv2.adaptiveThreshold(cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY), 
		255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,15,15)
	pts1,title = crop(thresh,[pts1,title])

	N = cv2.getPerspectiveTransform(title,pts3)
	heading = cv2.warpPerspective(frame,N,(450,120))
	cv2.imshow('heading',heading)

	M = cv2.getPerspectiveTransform(pts1,pts2)
	keyboard = cv2.warpPerspective(frame,M,(640,480))
	if not (pts1-pts2).any():
		continue
	file_p = (pytesseract.image_to_string(heading).lower()).replace('\n', '')

	if re.search('^keyboard(?:[123456890]{1})$',file_p):
		old_file,new_file = new_file,file_p

		if old_file!=new_file:
			print('NEW KEYBOARD DETECTED')
			_,board = cv2.threshold(cv2.warpPerspective(thresh,M,(640,480)),
			 100, 255, cv2.THRESH_BINARY_INV)
			text,location = extract(board,new_file)

	frame = cv2.rectangle(frame,(0,0),(640,50),(0,0,0),-1)
	frame = cv2.rectangle(frame,(0,400),(640,480),(0,0,0),-1)
	pointers = mask(keyboard)    

	contours,_ = cv2.findContours(pointers,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
	r = 0
	for c in contours: 
		x,y,w,h = cv2.boundingRect(c)
		if w*h <200:
			continue
		cv2.rectangle(keyboard,(x,y),(x+w,y+h),(0,255,0),2)
		m = list(filter(lambda i : y>location[i][0][1] and y<location[i][1][1],range(len(location))))
		n = list(filter(lambda i: x>location[i][0][0] and x<location[i][1][0],m))
		if len(n)==1:
			touched.update(n)
			if text[n[0]].isascii():
				cv2.putText(frame,text[n[0]],(5+r,40),cv2.FONT_HERSHEY_PLAIN,3,(255,255,255),3)
				r += 30

	if count% 6 == 5:
		pressed = touched.intersection(touched_1)
		touched_1 = touched
	if len(pressed)==1 and text[list(pressed)[0]]=='↑':
		caps = not caps
	else:
		(typed,shift) = display(pressed, text, frame, typed, shift,caps)

	cv2.putText(frame,typed+'|',(0,460),cv2.FONT_HERSHEY_SIMPLEX,2,(255,255,255),3)
	if caps:
		cv2.putText(frame,'CAPSLOCK ON',(400,30),cv2.FONT_HERSHEY_PLAIN,2,(0,0,255),2)
	else:
		cv2.putText(frame,'CAPSLOCK OFF',(400,30),cv2.FONT_HERSHEY_PLAIN,2,(0,0,255),2)	

	cv2.imshow('keyboard',keyboard)
	cv2.imshow('frame',frame)
	out.write(frame)
	count+=1
	if cv2.waitKey(10) == ord('q'):
		break

cv2.destroyAllWindows()
cap.release()
out.release()