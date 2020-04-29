import cv2 as cv 
import numpy as np 				

def nothing(x):                                                 # A dummy callback function for the Trackbar position change
	pass                                                    # Do nothing inside the function

img = cv.resize(cv.imread('1.jpeg'),(500,500))                                   # Reading the image and storing it in the variable 'img'
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)                      # Converting the image to grayscale mode

edges = cv.Canny(gray, 150, 150)               # Canny Edge Detection
cv.imshow('edges', edges)                                       # Display the edges obtained using the above algorithm

cv.namedWindow('image')                                         # Creating a named window 
cv.createTrackbar('threshold', 'image', 100, 300, nothing)      # Creating a Trackbar with 'threshold' label
flag=2

while(1):
				# To display the image consistently
	cv.imshow('image', img)					# The generated lines are displayed on the image itself
	k = cv.waitKey(1)					# Waits for the user to press a key for 1 ms.
	if k == 27:					        # If 'escape' key is pressed, the loop is terminated
		break
	img = cv.imread('sudoku.png')				# The image is read into the img variable

	thresh = cv.getTrackbarPos('threshold', 'image')	# Obtaining the value of the Trackbar
	lines = cv.HoughLines(edges, 1, np.pi/180, 100)	# Obtaining the lines using the HoughLines Function

	for line in lines:					# Iterating over the lines obtained
		rho, theta = line[0]			        # Obtaining the r, theta of the line
		a = np.cos(theta)				# Evaluating cos theta
		b = np.sin(theta)				# Evaluating sin theta
		x0 = a*rho					# Obtaining the perpendicular distant x co-ordinate
		y0 = b*rho					# Obtaining the perpendicular distant y co-ordinate
		x1 = int(x0 + 100*(-b))			# Specifying x co-ordinate of one end of the line 
		y1 = int(y0 + 100*a)				# Specifying y co-ordinate of one end of the line
		x2 = int(x0 + 100*b)				# Specifying x co-ordinate of the other end of the line
		y2 = int(y0 + 100*(-a))			# Specifying y co-ordinate of the other end of the line
		cv.line(img, (x1,y1), (x2,y2), (0,0,255), 2)	# Drawing the line

cv.destroyAllWindows()						# Closing all the windows and terminate the program