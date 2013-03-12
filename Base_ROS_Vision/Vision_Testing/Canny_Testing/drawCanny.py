

import cv2
import numpy as np
from random import random
def main():
	cv2.namedWindow("Original",0)
	cv2.namedWindow("Canny",0)
	cv2.namedWindow("DiffCan",0)
	cap=cv2.VideoCapture(0);

	(valid_frame,frame) = cap.read()
	t1 = 0;
	t2 = 1;
	ap  = 3;
	ap2 = 5;

	while(1):
		(valid_frame,frame) = cap.read()
		frame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
		canned = cv2.Canny(	image = frame, \
							threshold1 = t1, \
							threshold2 = t2, \
							apertureSize = ap, \
							L2gradient = True)
		canned2 = cv2.Canny(image = frame, \
							threshold1 = t1, \
							threshold2 = t2, \
							apertureSize = ap2, \
							L2gradient = True)
		diff = cv2.subtract(canned,canned2)
		cv2.imshow("Original",frame)
		cv2.imshow("Canny",canned)
		cv2.imshow("DiffCan",diff)
		key_pressed = cv2.waitKey(5)
		if( key_pressed == 27 ):
			return 0
		elif( key_pressed == 49 ):
			t2 = random()*255
			t1 = random()*(t2)
			print "[",t1,",",t2,"]"
		elif( key_pressed == 50 ):
			ap = int(random()*3)*2+3
			print "ap = ",ap
		elif( key_pressed == 51 ):
			t2 = min((t2+random()*40-20),255)
			t1 = random()*(t2)
			print "[",t1,",",t2,"]"
		elif( key_pressed == 53 ):
			t1 = t1+1
			if( t1 >= t2 ):
				t2 = t2 +1
				t1 = 0
			####
			print "[",t1,",",t2,"]"
		elif( key_pressed == 54 ):
			t1 = t1+10
			if( t1 >= t2 ):
				t2 = t2 +1
				t1 = 0
			####
			print "[",t1,",",t2,"]"
		####
####


if __name__=="__main__":
	main()
####
