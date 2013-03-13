
import cv2
import numpy as np
from sys import argv
from random import random

##
## Input Binary Image
##	for each contour found
##	display in a window
##

"""This program will take an image and display each external contour
in a separate window and with a different color. Try using the test image
"/secon2013/Base_ROS_Vision/Vision_Testing/Draw_Contours/external_contour_test.png"
"""
def main():

	if( argv.__len__()!= 2):
		print "\nError\nUsage *.py (image)"
		return -1
	####
	fileName = argv[1]
	img = cv2.imread(fileName)
	print "cats",img.ndim
	if( img == None ):
		print "\nError\nCould not open file <",fileName,">"
		return -1
	####
	img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	print "cats",img.ndim
	
	(contours,hierarchy) = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
	i = 0;

	"""
	for contour in contours:
		cv2.namedWindow("Contour #"+str(i))
		canvas = np.zeros_like(img)
		kittens = cv2.merge([canvas,canvas,canvas])
		print i," ",canvas.ndim
		cv2.drawContours(image = kittens, \
						contours = contour, \
						contourIdx = -1, \
						color = (255,255,255),
						thickness =-1)
		cv2.imshow("Contour #"+str(i),kittens)
		i = i+1
	####
"""
	cv2.namedWindow("Contours")
	canvas = np.zeros_like(img);
	kittens = cv2.merge([canvas,canvas,canvas])
	for contour in contours:
		cv2.drawContours(kittens,[contour],-1,(random()*255,random()*255,random()*255),-1)
	####
	cv2.imshow("Contours",kittens)
	while(1):
		keyPress = cv2.waitKey(10)
		if keyPress == 27:
			return 0
		####
	####
	return 0
####

####


if __name__=="__main__":
	main()
####
