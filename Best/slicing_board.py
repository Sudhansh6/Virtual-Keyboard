import cv2
import numpy as np
from keras.models import load_model
import pickle
def nothing(x): pass

cap = cv2.VideoCapture(2)
dst = np.ones((640,480))
size = 32
flag =1
while(True):
	# board = cv2.resize(cv2.imread('sudoku1.jpeg'),(360,540))

	_,board = cap.read()
	h,w = board.shape[:2]

	gray = cv2.cvtColor(board,cv2.COLOR_BGR2GRAY)
	board_thresh = gray
	thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
			 cv2.THRESH_BINARY_INV,5, 2)
	opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, np.ones((3,3),np.int8))
	dilated = cv2.dilate(opening,np.ones((3,3),np.int8),6)


	lines = cv2.HoughLinesP(dilated,1,np.pi/180,threshold = 80,minLineLength = 150,maxLineGap = 20)
	threshc = thresh.copy()
	try:
		N = lines.shape[0]
		for i in range(N):
		    x1 = lines[i][0][0]
		    y1 = lines[i][0][1]    
		    x2 = lines[i][0][2]
		    y2 = lines[i][0][3]    
		    threshc = cv2.line(threshc,(x1,y1),(x2,y2),(255,255,255),4)
	except:
		pass
	cv2.imshow('lines',threshc)
	contours,_ = cv2.findContours(threshc,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
	cnt = sorted(contours, key=lambda x: cv2.contourArea(x),reverse = True)[0]

	a = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True)
	maximum = thresh.copy()
	cv2.drawContours(maximum, cnt, -1, (255,255,255), 10)
	cv2.imshow('max', maximum)
	
	if(len(a)==4):	
		b=np.zeros(4)
		for i in range(4):
			b[i]= a[i][0][0]+a[i][0][1]

		c = np.argsort(b)

		if(a[c[1]][0][0] < a[c[2]][0][0]):
			tmp = c[2]
			c[2],c[1] = c[1],tmp
		pts1 = np.array([a[c[0]][0]-5,a[c[1]][0],a[c[3]][0],a[c[2]][0]],np.float32)
		pts2 = np.array([[0,0],[500,0],[500,500],[0,500]],np.float32)

		M = cv2.getPerspectiveTransform(pts1,pts2)
		board_cropped = cv2.warpPerspective(board_thresh,M,(500,500))
		thresh_cropped = cv2.warpPerspective(thresh,M,(500,500))
		# cv2.imshow('thresh_cropped',thresh_cropped)
		contour_board,_ = cv2.findContours(thresh_cropped,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
		cntb = sorted(contour_board, key=lambda x: cv2.contourArea(x),reverse = True)[0]
		a = cv2.approxPolyDP(cntb,0.01*cv2.arcLength(cntb,True),True)
		maximumb = board_cropped.copy()
		cv2.drawContours(maximumb, cntb, -1, (255,255,2), 10)
		cv2.imshow('contours',maximumb)
		if(len(a)==4 and flag):	
			print('\n==========',flag,'============\n')
			flag+=1
			# flag =0
			b=np.zeros(4)
			for i in range(4):
				b[i]= a[i][0][0]+a[i][0][1]
			c = np.argsort(b)
			X,Y = a[c[3]][0]
			board_cropped = board_cropped[5:Y-5,5:X-5]
			thresh_cropped = thresh_cropped[5:Y-5,5:X-5]
			x,y = X//9,Y//9
			number,t_number = [],[]
			for i in range(9):
				for j in range(9):
					e = 10
					y1 = i*y+e
					y2 = (i+1)*y-e
					x1 = j*x+e
					x2 = (j+1)*x-e
					# print(y1,y2,x1,x2)
					img = cv2.resize(board_cropped[y1:y2,x1:x2],(size,size)).copy()
					# img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
			 # cv2.THRESH_BINARY,7, 5)
					img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
					t_img = cv2.resize(thresh_cropped[y1:y2,x1:x2],(size,size)).copy()
					t_number.append(t_img)
					# img = cv2.rectangle(img, (2,2), (size-2,size-2), (255,255,255),2)
					number.append(img)
				i,j = 0,1		
			
			model = load_model('simple_nn.model')
			lb = pickle.loads(open('simple_nn_lb.pickle', "rb").read())

			for m in range(0,3):
				for n in range(0,3):
					cv2.imshow(str(m+1)+'X'+str(n+1),number[m*9+n])
					number[m*9+n] = number[m*9+n].astype("float") / 255.0
					number[m*9+n] = number[m*9+n].flatten()
					number[m*9+n] = number[m*9+n].reshape((1, number[m*9+n].shape[0]))
					xyz = t_number[m*9+n].copy()
					cv2.GaussianBlur(xyz,(7,7),10)
					_, th1 = cv2.threshold(xyz, 240, 255, cv2.THRESH_BINARY)

					# th1 = th1[size//2-size//16:size//2+size//16,size//2-size//16:size//2+size//16]
					# print(th1,"\n")
					if(np.sum(th1>0)>30):
						# cv2.imshow(str(m)+'x'+str(n),t_number[m*9+n])
						# print(m,n)
						prediction = model.predict(number[m*9+n])
						i = prediction.argmax(axis=1)[0]
						label = lb.classes_[i]
						print(str(m+1)+"X"+str(n+1)+" = "+str(label))

		cv2.warpPerspective(board,M,(w,h),board, cv2.WARP_INVERSE_MAP,cv2.BORDER_TRANSPARENT)
	# cv2.imshow('putback',board)
	if (cv2.waitKey(100)==ord('q') ):#or True):
		break
if (cv2.waitKey(0)==ord('q')):
	cv2.destroyAllWindows()
