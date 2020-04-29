import cv2
import numpy as np

def nothing(x): pass

cap = cv2.VideoCapture(-1) # Start Video Capture
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi',fourcc,20,(640,480))

while(True):
	_,board = cap.read()
	h,w = board.shape[:2]
#	CONVERT TO GRAYSCALE, BLUR AND APPLY ADAPTIVE THRESHOLD
	gray = cv2.cvtColor(board,cv2.COLOR_BGR2GRAY)
	blur = cv2.GaussianBlur(gray,(5,5),0)
	thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
			 cv2.THRESH_BINARY_INV,7, 2); 
#	DETECT EDGES AND DRAW APPROXIMATE LINES
#	NOTE: observed to work better without it.
# 	edges = cv2.Canny(thresh,400,50,apertureSize = 3)
# 	cv2.imshow('edges',edges)

# 	lines = cv2.HoughLinesP(edges,1,np.pi/180,threshold = 600,minLineLength = 200,maxLineGap = 30)
# 	edges = cv2.cvtColor(edges,cv2.COLOR_GRAY2BGR)
# 	N = lines.shape[0]
# 	for i in range(N):
# 	    x1 = lines[i][0][0]
# 	    y1 = lines[i][0][1]    
# 	    x2 = lines[i][0][2]
# 	    y2 = lines[i][0][3]    
# 	    cv2.line(edges,(x1,y1),(x2,y2),(255,0,255),2)
# 	edges = cv2.cvtColor(edges,cv2.COLOR_BGR2GRAY)

#	FIND CONTOUR HAVING LARGEST AREA AND FIND ITS SHAPE
	contours,_ = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
	cnt = sorted(contours, key=lambda x: cv2.contourArea(x),reverse = True)[0]
	a = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True)
	b=np.zeros(4)

	if(len(a)==4):	# CHECK IF IT IS A QUADRILATERAL
		for i in range(4):
			b[i]= a[i][0][0]+a[i][0][1]
#		SORT IT SUCH THAT THE POINTS ARE IN ANTICLOCKWISE ORDER
		c = np.argsort(b)
		if(a[c[1]][0][0] < a[c[2]][0][0]):
			tmp = c[2]
			c[2],c[1] = c[1],tmp
#		MAKE LISTS OF POINTS OF CORNERS OF BOARD AND IMAGE			
		pts1 = np.array([a[c[0]][0],a[c[1]][0],a[c[3]][0],a[c[2]][0]],np.float32)
		pts2 = np.array([[0,0],[w,0],[w,h],[0,h]],np.float32)
#		GET OART OF IMAGE CONTAINING THE BOARD
		M = cv2.getPerspectiveTransform(pts1,pts2)
		dst = cv2.warpPerspective(board,M,(650,500))
		dst = cv2.putText(dst,'TEXT',(30,300),cv2.FONT_HERSHEY_SIMPLEX,3,(0,0,0),5)
#		SOLVE THE BOARD HERE
#		PUT THE BOARD BACK IN ORIGINAL IMAGE
		cv2.warpPerspective(dst,M,(w,h),board, cv2.WARP_INVERSE_MAP,cv2.BORDER_TRANSPARENT)
	
	cv2.imshow('SUDOKU',board)
	out.write(board)

	if (cv2.waitKey(10)==ord('q')):
		break
	
cap.release()	
out.release()
cv2.destroyAllWindows()
