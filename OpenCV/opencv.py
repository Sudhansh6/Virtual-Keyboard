import cv2 
from matplotlib import pyplot as plt

image = cv2.imread('pic.jpg') # putting (name,0) reads in grayscale mode
print('open')
h, w = image.shape[:2] 
print(h,w)
# OpenCV arranges the channels in BGR order
(B, G, R) = image[100, 100] # at 100,100 pixel
B = image[100,100,0]
region = image[25:75,45:65]
resized_image = cv2.resize(image, (800, 800))
# cv2.imshow('image',image)
# k = cv2.waitKey(0) & 0XFF
# if(k==27):
# 	cv2.destroyAllWindows()


center = (h//2,w//2)
matrix = cv2.getRotationMatrix2D(center, -45, 1.0)
# (center, angle, scale)
rotated = cv2.warpAffine(image, matrix, (2*w, 2*h))
# cv2.imshow('image',rotated)
# k = cv2.waitKey(0) & 0XFF
# if(k==27):
# 	cv2.destroyAllWindows()

output = image.copy()
rectangle = cv2.rectangle(output, (150, 90),(60, 40), (255, 0, 0), 2) 
# Image, Top-left corner, Bottom-right corner,Color (in BGR format),Line width
# cv2.imshow('image',rectangle)
# k = cv2.waitKey(0) & 0XFF
# if(k==27):
# 	cv2.destroyAllWindows()

text = cv2.putText(output, 'OpenCV Demo', (50, 55),cv2.FONT_HERSHEY_SIMPLEX,1	, (255, 0, 0), 2)
# Image, Text, Bottom-left corner, Font, Font size, Color (BGR format), Line width
cv2.imshow('image',rotated)
k = cv2.waitKey(0) & 0XFF
if(k==27):
	cv2.destroyAllWindows()

elif k == ord('s'):  
    cv2.imwrite('output.png',text) 
    cv2.destroyAllWindows() 

# Change the current directory  
# to specified directory  
# os.chdir(directory) directory is address like r '~home/So..'
  
# List files and directories   
# in 'C:/Users/Rajnish/Desktop/GeeksforGeeks'   
# print("Before saving image:")   
# print(os.listdir(directory))

