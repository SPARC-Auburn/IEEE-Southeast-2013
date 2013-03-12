
import cv2
import numpy as np
from sys import argv


def catsKey():
	while(1):
		keyPressed = cv2.waitKey(30)
		if( keyPressed == 48 ):
			return 0
		####
	####
####

def main():
	
	if( argv.__len__()!= 2 ):
		print "\nError\nUsage: *.py (fileName)"
		return -1
	####
	fileName = argv[1]
	img = cv2.imread(fileName)

	if( img == None ):
		print "\nError\ncould not open <",fileName,">"
		return -1
	####

	color_dict = {"red":(0,0,255),"orange":(0,88,220,),"yellow":(0,255,255),"green":(0,255,0),"blue":(255,0,0),"brown":(0,50,108)}

	KERNEL = np.ones((3,3),np.uint8)
	red_low_1  = np.array([135,110,33])
	red_high_1 = np.array([180,230,230])
	red_low_2  = np.array([0,110,33])
	red_high_2 = np.array([0,230,230])

	orange_low  = np.array([3,120,55])
	orange_high = np.array([16,230,230])

	yellow_low  = np.array([23,55,110]) 
	yellow_high = np.array([32,255,255])

	green_low  = np.array([50,55,55])
	green_high = np.array([80,230,230])

	blue_low  = np.array([100,110,55])
	blue_high = np.array([120,220,220])

	brown_low  = np.array([37,20,20]) 
	brown_high = np.array([43,50,50])

	cv2.namedWindow("canned")

	print "Gray Image"
	img_gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	cv2.imshow("canned",img_gray)
	catsKey()

	print "Gaussian Blurred 9x9"
	img_gray = cv2.GaussianBlur(img_gray,(9,9),7)
	cv2.imshow("canned",img_gray)
	catsKey()

	print "Canny"
	img_canned =cv2.Canny( image = img_gray, \
				      threshold1 = 40, \
				      threshold2 = 220, \
				    apertureSize = 5, \
			          L2gradient = True)
	cv2.imshow("canned",img_gray)
	catsKey()
#	img_canned = cv2.dilate(img_canned,KERNEL,iterations=1)
#	img_canned = cv2.erode(img_canned,KERNEL,iterations=1)
	
	print "Gaussian Blurred 5x5"
	img_canned = cv2.GaussianBlur(img_canned,(5,5),0)
	cv2.imshow("canned",img_gray)
	catsKey()

	cats,img_canned = cv2.threshold(img_canned,64,255,cv2.THRESH_BINARY)
#	img_canned = cv2.erode(img_canned,KERNEL)
	img_canned = cv2.bitwise_not(img_canned)
	cv2.imshow("canned",img_canned)
	catsKey()
	img_hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV);

	red_image1 = cv2.inRange(img_hsv,red_low_1,red_high_1)
	red_image2 = cv2.inRange(img_hsv,red_low_2,red_high_2)
	red_image = cv2.bitwise_or(red_image1,red_image2)

	orange_image = cv2.inRange(img_hsv,orange_low,orange_high)

	yellow_image = cv2.inRange(img_hsv,yellow_low,yellow_high)

	green_image	 = cv2.inRange(img_hsv,green_low,green_high)

	blue_image = cv2.inRange(img_hsv,blue_low,blue_high)

	brown_image = cv2.inRange(img_hsv,brown_low,brown_high)

	d = {"red":red_image,"orange":orange_image,"yellow":yellow_image,"green":green_image,"blue":blue_image,"brown":brown_image}

	for key in d:
		cv2.namedWindow(key)
	####

	KERNEL = np.ones((3,3),np.uint8)
	print "Color Thresholded"
	for (key,value) in d.items():
		cv2.imshow(key,value)
	####
	catsKey()

	print "Eroded"
	for (key,value) in d.items():
		value = cv2.erode(value,KERNEL,iterations=1)
		cv2.imshow(key,value)
	####
	catsKey()

	print "Gaussian Blurred 5x5"
	for (key,value) in d.items():
		value = cv2.GaussianBlur(value,(5,5),5)
		cv2.imshow(key,value)
	####
	catsKey()

	print "Dilated"
	for (key,value) in d.items():
		value = cv2.dilate(value,KERNEL,iterations=3)
		cv2.imshow(key,value)
	####
	catsKey()

	print "Gaussian Blurred 5x5"
	for (key,value) in d.items():
		value = cv2.GaussianBlur(value,(5,5),5)
		cv2.imshow(key,value)
	####
	catsKey()

	print "Binary Thresholded"
	for (key,value) in d.items():
		cats,value = cv2.threshold(value,128,255,cv2.THRESH_BINARY)
		cv2.imshow(key,value)
	####
	catsKey()

	for (key,value) in d.items():
		(contours,hierarchy) = cv2.findContours(value,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
		for contour in contours:
			if contour.__len__()>=5:
				ellipse = cv2.fitEllipse(contour)
				cv2.ellipse(img,ellipse,color_dict[key],2)
			####
		####
	####
	cv2.namedWindow("cats")
	cv2.imshow("cats",img)

#	(contours,hierarchy) = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)

	while(1):
		keyPressed = cv2.waitKey(20)
		if( keyPressed == 27 ):
			return 0
		####
	####
####

if __name__=="__main__":
	main()
####



