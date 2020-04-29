import cv2 
import numpy as np


video = cv2.VideoCapture(-1) # Write the file name instead of number to see an existing video


while(True): # video.isOpened()

	ret,frame = video.read()
	cv2.imshow('frame',frame)
#h,w = video.get(cv2.CAP_PROP_FRAME_HEIGHT),video.get(cv2.CAP_PROP_FRAME_WIDTH)
	if cv2.waitKey(1) & 0XFF == ord('q'):
		break

video.release()
cv2.destroyAllWindows() 

# use cap.get('') to get details
# fourcc = cap.VideoWriter_fourcc(*'XVID')
# out = cap.VideoWriter('name.ext',20,(640,480))