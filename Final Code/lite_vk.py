import cv2
import numpy as np

def mask(frame):
	'''
	This function masks the frame and returns the picture
	which has only pointers visible
	'''
	try:
		f = open('hsv_values.txt','r') # check if hsv values are present
		h,s,v,H,S,V = list(int(x.replace('\n','')) for x in f)
		f.close()
	except:
		# Approx values of a fingernail
		h,s,v = 108, 61, 23
		H,S,V = 255,180,180

	low = np.array([h,s,v]) 
	high = np.array([H,S,V]) 
	frame = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV) 
	mask = cv2.inRange(frame,low,high) # Create a mask with low and high filters
	opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((7,7),np.int8),10)
	return opening

def crop(thresh,frame,pts1):
	'''
	This function returns the coordiantes of 
	corners of keyboard for changing perspective.
	'''
	contours,_ = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
	cnts = sorted(contours, key=lambda x: cv2.contourArea(x),reverse = True)[0]
	a = cv2.approxPolyDP(cnts,0.01*cv2.arcLength(cnts,True),True)
	if(len(a)==4):
		a = a.reshape(-1,2)
		c = np.argsort(np.sum(a,axis = 1))
		if(a[c[1]][0] < a[c[2]][0]):
			c[2],c[1] = c[1],c[2]
		c[2],c[3]=c[3],c[2]
		pts1 = np.float32(a[c])	
	return (pts1,contours)

def extract(keyboard):
	'''
	This function takes the keyboard layout as input.
	It detects the top-left and bottomr-right corners
	of every key and appends them to a list. It also reads
	the key at each location from a manually written text file.
	'''
	print("Extracting keys from keyboard")
	images,location = [],[]
	kcontours,_ = cv2.findContours(keyboard,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
	for cnt in kcontours:
		cnt_len = cv2.arcLength(cnt, True)
		cnt = cv2.approxPolyDP(cnt, 0.02*cnt_len, True)
		if len(cnt) == 4 and 12000>cv2.contourArea(cnt) and cv2.contourArea(cnt)> 400 and cv2.isContourConvex(cnt):
			a = cnt.reshape(-1, 2)
			c = np.argsort(np.sum(a,axis = 1))
			if(a[c[1]][0] < a[c[2]][0]):
				c[2],c[1] = c[1],c[2]
			c[2],c[3]=c[3],c[2]
			pts1 = np.float32(a[c])
			pts2 = np.float32([[0,0],[300,0],[300,300],[0,300]])
			M = cv2.getPerspectiveTransform(pts1,pts2)
			dst = cv2.warpPerspective(keyboard,M,(300,300))
			images.append(dst.copy())
			location.append((a[c[0]],a[c[2]]))
	print('Extracted')
	# Sorts the location linearly from top to bottom then left to right
	images,location = zip(*sorted(zip(images,location),key = lambda x: (x[1][0][1]//40,x[1][0][0])))
	f = open('keyboard4.txt')
	data = f.read().replace('\n', '')
	f.close()

	return (images,data,np.array(location))

def display(pressed,text,frame,typed,shift,caps):
	'''
	This function takes the pressed keys as input 
	and displays them accordingly on the frame
	'''
	for i in pressed:
		if(text[i]=='←'): 
			typed = typed[:-1]
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


cap = cv2.VideoCapture(-2)
count,flag,shift,caps = 0,1,False,True
pts1 = np.float32([[0,0],[640,0],[640,480],[0,480]])
pts2 = np.float32([[0,0],[640,0],[640,480],[0,480]])
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output_lite.avi',fourcc,20,(640,480))

while(True):
	_,frame = cap.read()
	touched = set()
	pressed = set()
	CAPS = set()
	if not count:
		h,w = frame.shape[:2]
		touched_1 = set()
		touched_2 = set()
		typed,text = '',''
	# Pre processing for crop function.
	gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
	thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
			 cv2.THRESH_BINARY_INV,15,15)

	pts1,contours = crop(thresh,frame,pts1)
	# Change perspective to get the keyboard.
	M = cv2.getPerspectiveTransform(pts1,pts2)
	keyboard = cv2.warpPerspective(frame,M,(640,480))
	if (pts1-pts2).any() and flag:
		t_keyboard = cv2.warpPerspective(thresh,M,(640,480))
		flag = 0
		_,board = cv2.threshold(t_keyboard, 100, 255, cv2.THRESH_BINARY_INV)
		images,text,location = extract(board)
		l = len(location)
	# Draw rectangles on frame to keep track of states like caps, touched keys and text.
	frame = cv2.rectangle(frame,(0,0),(640,50),(0,0,0),-1)
	frame = cv2.rectangle(frame,(0,400),(640,480),(0,0,0),-1)
	pointers = mask(keyboard)
	# Detects contours around each pointer (fingers)
	contours,_ = cv2.findContours(pointers,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
	pointers = cv2.cvtColor(pointers,cv2.COLOR_GRAY2BGR)
	i = 0
	for c in contours: 
		x,y,w,h = cv2.boundingRect(c)
		# if contour is of considerable size, determine its location.
		if w*h >200:
			cv2.rectangle(pointers,(x,y),(x+w,y+h),(0,255,0),2)
			cv2.rectangle(keyboard,(x,y),(x+w,y+h),(0,255,0),2)
			try:
				m = list(filter(lambda i : y>location[i][0][1] and y<location[i][1][1],range(l)))
				n = list(filter(lambda i: x>location[i][0][0] and x<location[i][1][0],m))
				# Add the key to touched list
				if len(n)==1:
					touched.update(n)
					if text[n[0]].isascii():
						string = text[n[0]]
						cv2.putText(frame,string,(5+i,40),cv2.FONT_HERSHEY_PLAIN,3,(255,255,255),3)
						i += 30
			except:
				pass
	if count% 15 == 5:
		# Check the commonly touched keys every ~150 ms
		if len(pressed) and text[list(pressed)[0]]=='↑':
			caps = not caps
		else:
		# The common keys touched in the interval were pressed.
		# Add them to pressed list.
			pressed = touched.intersection(touched_1)
		touched_1 = touched
	# Give the keys to display on frame (else print)
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
print('')
cv2.destroyAllWindows()
cap.release()
out.release()
