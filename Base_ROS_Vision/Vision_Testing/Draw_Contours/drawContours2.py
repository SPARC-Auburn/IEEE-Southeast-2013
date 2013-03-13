
import cv2
import numpy as np
from random import random

"""Second attempt at drawing contours on an image. Once again 
opencv2 1, pat 0

yeah, the "orange" isn't orange I think it is blue.

Anyways this thing just draws a bunch of annoying rainbow colored blob outlines.
Carry on...
"""

def main():
	cv2.namedWindow("Original",0)
	cv2.namedWindow("HSV",0)
	cv2.namedWindow("Contours",0)
	cv2.namedWindow("Blob",0)

	capture=cv2.VideoCapture(0);

	(valid_frame,frame) = capture.read()
	
	frame_hsv = np.zeros_like(frame)

	ORANGE_MIN = np.array([110,10,10],np.uint8)
	ORANGE_MAX = np.array([140,255,255],np.uint8)

	COLOR = np.array([255,0,0],np.uint8)
	KERNEL = np.ones((3,3),np.uint8)
	meow = -5
	while(1):
		(valid_frame,frame) = capture.read()
		frame_hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
		
		blobs = cv2.inRange(frame_hsv,ORANGE_MIN,ORANGE_MAX)
		for i in xrange(4):
			blobs = cv2.erode(blobs,kernel=KERNEL)
			blobs = cv2.GaussianBlur(blobs,(5,5),0)
			blobs = cv2.dilate(blobs,kernel=KERNEL)
			blobs = cv2.GaussianBlur(blobs,(3,3),0)
		####
		cv2.imshow("Blob",blobs)
		(cats,blobs) = cv2.threshold(blobs,64,255,cv2.THRESH_BINARY)
		(contours,hierarchy) = cv2.findContours(blobs,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)

		kittens = cv2.merge([blobs,blobs,blobs])
		big_contours = [x for x in contours if cv2.contourArea(x)>1000]
		big_contours.sort(key=lambda x: cv2.contourArea(x),reverse=True)
		try:
			##max_area = cv2.contourArea(big_contours[0])
			##print "\nbegin"
			##print "number of contours: ",big_contours.__len__()
			##for ind in xrange(big_contours.__len__()):
			##	c = big_contours[ind]
			##	area = cv2.contourArea(c)
			##	print ind,":\n",area,c.size,c
			cv2.drawContours(kittens,contours,-1,(random()*255,random()*255,random()*255),0)
			kittens2=kittens.copy()
			cv2.drawContours(kittens2,np.array([[[50,50]],[[100,50]],[[50,100]]]),-1,(255,255,255),-1)
			##	break
			####
			cv2.imshow("Contours",kittens)
		except IndexError:
			pass
		####	

	##	cv2.drawContours(blobs, big_contours,contourIdx = -1, color = 128,thickness=1,lineType = cv2.CV_AA)

		b=np.array([[[0,0]],[[0,200]],[[200,0]]])
		cv2.drawContours(frame_hsv,b,-1,(255,255,255),-1)
		cv2.imshow("Original",kittens2)
		cv2.imshow("HSV",frame_hsv)
		"""
		cv.InRangeS(hsv_frame,cv.Scalar(43,50,50),cv.Scalar(70,255,255),hsv_mask)
		cv.Dilate(hsv_mask,hsv_mask,None,3)
		cv.Erode(hsv_mask,hsv_mask,None,3)
		cv.Set(temp,0)
		cv.Copy(hsv_frame,temp,hsv_mask)
		cv.CvtColor(temp,temp,cv.CV_HSV2BGR)
		cv.ShowImage("Original",frame)
		cv.ShowImage("HSV",temp)
		"""
		keyPress = cv2.waitKey(10)
		if keyPress == 27:
			return 0
		elif keyPress == 48:
			meow = meow +1
		####	
	####

####


if __name__=="__main__":
	main()
####
