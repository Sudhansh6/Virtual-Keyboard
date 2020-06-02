import cv2
import numpy as np

def nothing(x): pass

cap = cv2.VideoCapture(-1)
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi',fourcc,20,(640,480))

while(True):
	# board = cv2.resize(cv2.imread('sudoku.jpeg'),(360,540))
	_,board = cap.read()
	h,w = board.shape[:2]

	gray = cv2.cvtColor(board,cv2.COLOR_BGR2GRAY)
	cv2.imshow('gray',gray)

	blur = cv2.GaussianBlur(gray,(5,5),0)
	#cv2.imshow('blur',blur)

	thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
			 cv2.THRESH_BINARY_INV,7, 2);
	cv2.imshow('thresh',thresh)

	edges = cv2.Canny(thresh,400,50,apertureSize = 3)
	# edges = cv2.medianBlur(edges,7)
	cv2.imshow('edges',edges)
	edges = thresh

	# lines = cv2.HoughLinesP(edges,1,np.pi/180,threshold = 600,minLineLength = 200,maxLineGap = 30)
	# edges = cv2.cvtColor(edges,cv2.COLOR_GRAY2BGR)
	# N = lines.shape[0]
	# for i in range(N):
	#     x1 = lines[i][0][0]
	#     y1 = lines[i][0][1]    
	#     x2 = lines[i][0][2]
	#     y2 = lines[i][0][3]    
	#     cv2.line(edges,(x1,y1),(x2,y2),(255,0,255),2)

	# cv2.imshow('lines',edges)
	# edges = cv2.cvtColor(edges,cv2.COLOR_BGR2GRAY)
	contours,_ = cv2.findContours(edges,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
	#contoursc = cv2.drawContours(edges, contours, -1, (255,255,255), 3)
	#cv2.imshow('contours',contoursc)

	# areas = [cv2.contourArea(c) for c in contours]
	# max_index = np.argmax(areas)
	# cnt=contours[max_index]

	# cnts = cnts[0] if imutils.is_cv2() else cnts[1]  
	cnt = sorted(contours, key=lambda x: cv2.contourArea(x),reverse = True)[0]

	a = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True)
	max = cv2.drawContours(thresh, cnt, -1, (255,255,255), 3)
	cv2.imshow('max',max)
	# print(a)
	b=np.zeros(4)
	dst = thresh
	if(len(a)==4):	
		for i in range(4):
			b[i]= a[i][0][0]+a[i][0][1]

		c = np.argsort(b)

		if(a[c[1]][0][0] < a[c[2]][0][0]):
			tmp = c[2]
			c[2],c[1] = c[1],tmp
		pts1 = np.array([a[c[0]][0],a[c[1]][0],a[c[3]][0],a[c[2]][0]],np.float32)
		pts2 = np.array([[0,0],[w,0],[w,h],[0,h]],np.float32)

		M = cv2.getPerspectiveTransform(pts1,pts2)
		dst = cv2.warpPerspective(board,M,(650,500))
		dst = cv2.putText(dst,'TEXT',(30,300),cv2.FONT_HERSHEY_SIMPLEX,3,(0,0,0),5)
		# M = cv2.getPerspectiveTransform(pts2,pts1)
		cv2.warpPerspective(dst,M,(w,h),board, cv2.WARP_INVERSE_MAP,cv2.BORDER_TRANSPARENT)
		# arr = np.where(gray!=0)
		# board[arr] = gray [arr]
	cv2.imshow('putback',board)
	cv2.imshow('final',dst)
	out.write(board)

	if (cv2.waitKey(100)==ord('q')):
		break
	
cap.release()	
out.release()
cv2.destroyAllWindows()
