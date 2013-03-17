
import cv2
import numpy as np
import time
from sys import argv
from os import path,mkdir
"""This python program is meant to be the final BlockFinder program
it is still under construction

Note to future opencv2-ers cv2.findContours edits the image!
It edits the argument image. Ugh. 25 minutes wasted


"""

class BlockFinder():
	"""
	-Ignore everything above the strong line with black on the bottom side of the line
	-Ignore small bright spots 
	-Reduce the color space to only a couple colors
	-Look only at specified colors
	-Find only external contours of stuff
	--in other words look at blobs that have different colored edges. Not same colors on both sides.
	-Count the number of blobs

	"""
	def __init__(self):

		#########
		####Constants

		###Draft#2
		##HSV
		##color = (B,G,R)
		##lower/upperb =(Hue,Sat,Val)
		self.black_hsv_d2 = Threshold( name = "black", \
			color = (0,0,0), \
			lowerb = ( 16, 29,130), \
			upperb = (108,194,152) )
		self.red1_hsv_d2 = Threshold( name = "red1", \
			color = (0,0,255), \
			lowerb = ( 32,147,116), \
			upperb = ( 61,224,155) )
		self.red2_hsv_d2 = Threshold( name = "red2", \
			color = (0,0,255), \
			lowerb = (231,129, 89), \
			upperb = (159,238,166) )
		self.orange_hsv_d2 = Threshold( name = "orange", \
			color = (0,100,230), \
			lowerb = (  6,154, 47), \
			upperb = (218,222,101) )
		self.yellow_hsv_d2 = Threshold( name = "yellow", \
			color = (0,255,255), \
			lowerb = (  0,108,  0), \
			upperb = (255,143,101) )
		self.green_hsv_d2 = Threshold( name = "green", \
			color = (0,255,0), \
			lowerb = (  0,108, 82), \
			upperb = ( 60,123,130) )
		self.blue_hsv_d2 = Threshold( name = "blue", \
			color = (255,0,0), \
			lowerb = (  9,  0,154), \
			upperb = ( 78,255,254) )
		self.brown_hsv_d2 = Threshold( name = "brown", \
			color = (0,77,108), \
			lowerb = (  6,133, 18), \
			upperb = ( 27,205,236) )

		##YCR_CB
		##color = (B,G,R)
		##lower/upperb =(Y,ChrRed,ChrBlue)
		self.black_ycrcb_d2 = Threshold( name = "black", \
			color = (0,0,0), \
			lowerb = ( 15, 94,129), \
			upperb = ( 86,130,140) )
		self.red_ycrcb_d2 = Threshold( name = "red", \
			color = (0,0,255), \
			lowerb = (  6,139,118), \
			upperb = ( 72,195,126) )
		self.orange_ycrcb_d2 = Threshold( name = "orange", \
			color = (0,100,230), \
			lowerb = ( 41,154, 44), \
			upperb = (176,202,102) )
		self.yellow_ycrcb_d2 = Threshold( name = "yellow", \
			color = (0,255,255), \
			lowerb = ( 37,122, 14), \
			upperb = (243,141,108) )
		self.green_ycrcb_d2 = Threshold( name = "green", \
			color = (0,255,0), \
			lowerb = (  3, 98,109), \
			upperb = ( 37,124,130) )
		self.blue_ycrcb_d2 = Threshold( name = "blue", \
			color = (255,0,0), \
			lowerb = (  2, 74,154), \
			upperb = ( 43,143,129) )
		self.brown_ycrcb_d2 = Threshold( name = "brown", \
			color = (0,77,108), \
			lowerb = ( 14,133,127), \
			upperb = ( 43,143,129) )
		####


		###Draft #1
		##HSV
		##color = (B,G,R)
		##lower/upperb =(Hue,Sat,Val)
		self.black_hsv_d1 = Threshold( name = "black", \
								color = (0,0,0), \
								lowerb = (140,  0, 41), \
								upperb = (125, 39, 61) )
		self.red1_hsv_d1 = Threshold( name = "red1", \
								color = (0,0,255), \
								lowerb = (  0,165, 61), \
								upperb = (  6,212,126) )
		self.red2_hsv_d1 = Threshold( name = "red2", \
								color = (0,0,255), \
								lowerb = (169,165, 61), \
								upperb = (179,212,126) )
		self.orange_hsv_d1 = Threshold( name = "orange", \
								color = (0,100,230), \
								lowerb = (  4,186,108), \
								upperb = ( 13,255,255) )
		self.yellow_hsv_d1 = Threshold( name = "yellow", \
								color = (0,255,255), \
								lowerb = ( 21,148, 97), \
								upperb = ( 32,255,255) )
		self.green_hsv_d1 = Threshold( name = "green", \
								color = (0,255,0), \
								lowerb = ( 54, 74, 44), \
								upperb = ( 78,140, 77) )
		self.blue_hsv_d1 = Threshold( name = "blue", \
								color = (255,0,0), \
								lowerb = (108,168, 41), \
								upperb = (121,255,202) )
		self.brown_hsv_d1 = Threshold( name = "brown", \
								color = (0,77,108), \
								lowerb = (  2, 74, 51), \
								upperb = ( 15,204, 84) )

		##YCR_CB
		##color = (B,G,R)
		##lower/upperb =(Y,ChrRed,ChrBlue)
		self.black_ycrcb_d1 = Threshold( name = "black", \
								color = (0,0,0), \
								lowerb = ( 38,127,128), \
								upperb = ( 57,128,133) )
		self.red_ycrcb_d1 = Threshold( name = "red", \
								color = (0,0,255), \
								lowerb = ( 31,148,107), \
								upperb = ( 70,177,126) )
		self.orange_ycrcb_d1 = Threshold( name = "orange", \
								color = (0,100,230), \
								lowerb = ( 49,165, 62), \
								upperb = (162,200,106) )
		self.yellow_ycrcb_d1 = Threshold( name = "yellow", \
								color = (0,255,255), \
								lowerb = ( 78,137, 35), \
								upperb = (239,150, 90) )
		self.green_ycrcb_d1 = Threshold( name = "green", \
								color = (0,255,0), \
								lowerb = ( 36,110,119), \
								upperb = ( 64,123,128) )
		self.blue_ycrcb_d1 = Threshold( name = "blue", \
								color = (255,0,0), \
								lowerb = ( 18, 85,140), \
								upperb = (117,126,198) )
		self.brown_ycrcb_d1 = Threshold( name = "brown", \
								color = (0,77,108), \
								lowerb = ( 31,138,114), \
								upperb = ( 66,148,125) )
		########


		self.ycrcb_thresholds = [ self.black_ycrcb_d2, \
							self.red_ycrcb_d2, \
							self.orange_ycrcb_d2, \
							self.yellow_ycrcb_d2, \
							self.green_ycrcb_d2, \
							self.blue_ycrcb_d2, \
							self.brown_ycrcb_d2 ]

		self.hsv_thresholds = [ self.black_hsv_d2, \
							self.red1_hsv_d2, \
							self.red2_hsv_d2, \
							self.orange_hsv_d2, \
							self.yellow_hsv_d2, \
							self.green_hsv_d2, \
							self.blue_hsv_d2, \
							self.brown_hsv_d2 ]

		########
		##Check the arguments and grab the image
		self.cats="cats"

		if( argv.__len__()!= 3 ):
			raise Exception("\n\nERROR\nUsage: *.py store_results={0,1} (fileName)\n")
		####
		self.store_results = int(argv[1])
		fileName = argv[2]
		self.original = cv2.imread(fileName)

		if( self.original == None ):
			raise Exception("\nError\ncould not open <"+fileName+">")
		####
		########

		(workingdir,exec_ext) = path.split(path.realpath(__file__))
		self.curtim = int(time.time())
		self.prefix = workingdir + "/Thresholding_Testing_"+str(self.curtim)+"/"
		
		if( self.store_results == 1 ):
			mkdir(self.prefix)
		####

	####

	def run(self):
		img_med = self.medianFilter(self.original)
		self.img_ycrcb = cv2.cvtColor(img_med,cv2.COLOR_BGR2YCR_CB)
		self.img_hsv   = cv2.cvtColor(img_med,cv2.COLOR_BGR2HSV)
		
		self.findInitialMasks()


		(contours,hierarchy) = cv2.findContours( \
								image = self.blockMask.copy(), \
								mode = cv2.RETR_EXTERNAL, \
								method = cv2.CHAIN_APPROX_SIMPLE )
		canvas = self.blockMask.copy()
		canvas = cv2.merge((canvas,canvas,canvas))
		cv2.drawContours( image = canvas, \
						contours = contours, \
						contourIdx = -1, \
						color = (0,255,0), \
						thickness = 0, \
						lineType = cv2.CV_AA)
		
		sorted_contours = self.sortContoursByArea(contours)
		outputFile = open("contour_hull_solidarity_information.txt",'w')
		for (i,contour) in enumerate(sorted_contours):
			hull = cv2.convexHull(contour)

			cv2.drawContours( image = canvas, \
						contours = [hull], \
						contourIdx = -1, \
						color = (0,0,255), \
						thickness = 0, \
						lineType = cv2.CV_AA)


			cnt_area = cv2.contourArea(contour)
			hull_area = cv2.contourArea(hull)
			if( hull_area != 0 ):
				outputFile.write(str(i)+"\t"+str(cnt_area)+"\t"+str(hull_area)+"\tsolidarity: "+str(cnt_area/hull_area))
			else:
				outputFile.write(str(i)+"\t"+str(cnt_area)+"\t"+str(hull_area)+"\tsolidarity: n/a")
			####
		####
		self.showImage("contours for blockMask",canvas)
		cv2.imwrite("Contours_for_BlockMask.png",canvas)
		outputFile.close()

		self.waitForKeyPress()
		print "DONE!"
	####

	def showImage(self,str,img):
		cv2.namedWindow(str)
		cv2.imshow(str,img)
	####

	def storeThresholdedImage(self,t,orig):
		##Assume the image has already by blurred
		#t is a Threshold object
		img = orig.copy()
		threshed_img = cv2.inRange(src = img, \
							lowerb = t.lowerb, \
							upperb = t.upperb)
		thr_cpy = threshed_img.copy()
		(contours,hierarchy) = cv2.findContours( \
							image = thr_cpy, \
							mode = cv2.RETR_EXTERNAL, \
							method = cv2.CHAIN_APPROX_NONE)
		cv2.drawContours( image = img, \
							contours = contours, \
							contourIdx = -1, \
							color = t.color, \
							thickness = -1, \
							lineType = cv2.CV_AA)
		if( self.store_results == 0 ):
			cv2.namedWindow(t.name)
			cv2.imshow(t.name,threshed_img)
			self.waitForKeyPress()
		elif( self.store_results == 1):
			cv2.imwrite(self.prefix+t.name+".png",img)
		####
		return None
	####

	def sortContoursByArea(self,contours):
		area_contours = []
		for contour in contours:
			area_contours.append((cv2.contourArea(contour),contour))
		####
		area_contours.sort(key=lambda x: x[0],reverse = True)
		return np.array([x[1] for x in area_contours])
	####

	def findInitialMasks(self):
		thr_black_ycrcb = cv2.inRange(src = self.img_ycrcb, \
								lowerb = self.black_ycrcb_d2.lowerb, \
								upperb = self.black_ycrcb_d2.upperb )
		thr_low_sat =    cv2.inRange(src = self.img_hsv, \
								lowerb = np.array((0,0,0),np.uint8), \
								upperb = np.array((255,85,255),np.uint8) )
		(contours,hier) = cv2.findContours( \
							image = thr_black_ycrcb.copy(), \
							mode = cv2.RETR_EXTERNAL, \
							method = cv2.CHAIN_APPROX_SIMPLE )

		canvas = np.zeros_like(thr_black_ycrcb)

		sorted_contours = self.sortContoursByArea(contours)
		biggest_contour = sorted_contours[0]

		cv2.drawContours( image = canvas, \
						contours = [biggest_contour], \
						contourIdx = -1, \
						color = (255), \
						thickness = -1 )
	
		self.courseMask = canvas

		#blocks = not(thr_low_sat) || not(thr_black_ycrcb)
		#blocks = not( thr_low_sat && thr_black_ycrcb )
		possible_blocks = cv2.bitwise_not(cv2.bitwise_and(thr_low_sat,self.courseMask))
		blocks_on_course = cv2.bitwise_and(possible_blocks,self.courseMask)

		self.blockMask = blocks_on_course
		return 1
	####

	def fixSmallHoles(self,mask):
		"""
		Now defunct, as of Mar 17
		the ycrcb external contour is good enough...
		"""
		self.showImage("mask coming in...",mask)
		(contours,hier) = cv2.findContours( \
							image = mask.copy(), \
							mode = cv2.RETR_EXTERNAL, \
							method = cv2.CHAIN_APPROX_NONE )

		area_contours = []
		for contour in contours:
			area_contours.append((cv2.contourArea(contour),contour))
		####
		area_contours.sort(key = lambda x: x[0], reverse = True)

		biggest_contour = area_contours[0][1]
		hull = cv2.convexHull(points = biggest_contour,returnPoints=False)
		defects = cv2.convexityDefects(biggest_contour,hull)

		print defects
		print "\n\n"
		for (i,ind) in enumerate(hull.flatten()):
			print i,ind,biggest_contour[ind]
		####
		print "\n"
		img = mask
		cnt = biggest_contour

		repaired = []
		hull_cats = []
		for i in range(defects.shape[0]):
			s,e,f,d = defects[i,0]
			start = tuple(cnt[s][0])
			end = tuple(cnt[e][0])
			far = tuple(cnt[f][0])
#			cv2.line(img,start,end,96,2)

#			cv2.circle(img,start,5,200,-1)
#			cv2.circle(img,end,5,200,-1)

#			cv2.circle(img,far,5,128)
#			if( d > 5000):
#				cv2.circle(img,far,7,128)
#				cv2.circle(img,far,9,128)
#			####

			hull_cats.append(cnt[s].tolist())
			hull_cats.append(cnt[e].tolist())
			if( d > 5000):
				if( e < s):
					repaired.extend(cnt[s:].tolist())
					repaired.extend(cnt[:(e+1)].tolist())
				else:
					repaired.extend(cnt[s:(e+1)].tolist())
				####
			else:
				repaired.append(cnt[s].tolist())
				repaired.append(cnt[e].tolist())
			####
		####
		hull_cats = np.array(hull_cats)
		repaired = np.array(repaired)
		cv2.drawContours( image = mask, \
			contours = [hull_cats], \
			contourIdx = -1, \
			color = (128), \
			thickness = -1 )
		cv2.drawContours( image = mask, \
			contours = [repaired], \
			contourIdx = -1, \
			color = (250), \
			thickness = -1 )
		cv2.drawContours( image = mask, \
			contours = [biggest_contour], \
			contourIdx = -1, \
			color = (64), \
			thickness = 1 )
		self.showImage("mask with hull,repaired,and,biggestcontour",mask)	
		


		print "REPAIRED"
		for (i,ind) in enumerate(repaired):
			print i,ind
		####


		print "\n\nHULL_CATS"
		for (i,t) in enumerate(hull_cats):
			print i,t
		####

		self.showImage("IMAGE?",img)
		self.waitForKeyPress()
		assert False
		dist = lambda a,b: ((a[0]-b[0])**2+(a[1]-b[1])**2)
	####

	def medianFilter(self,img):
		tmp = img.copy()
		for i in xrange(15):
			tmp = cv2.medianBlur(tmp,3)
		####
		return tmp
	####

	def waitForKeyPress(self):
		while(1):
			keyPressed = cv2.waitKey(5)

			if( keyPressed == 27 ):
				raise Exception("\n\nQuit on ESC key\n")
			elif( keyPressed != -1 ):
				return keyPressed
			####
		####
	####

	def colorReduce(self,img,iter=1):
		i = 0xFF;
		for k in xrange(iter):
			img = np.bitwise_and(img,i)
			i = i - 2**k
		####
		return img
	####
####

def main():

	KERNEL = np.ones((3,3),np.uint8)

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

class Threshold():
	"""This class is just a glorified struct...
	name	:	string
	color	:	(3 tuple)
	lowerb	:	(3 tuple)
	upperb	:	(3 tuple)
	"""
	def __init__(self,name,color,lowerb,upperb):
		self.name = name
		self.color = color
		self.lowerb = np.array(lowerb,np.uint8)
		self.upperb = np.array(upperb,np.uint8)
	####

	def __str__(self):
		return '\t'.join([str(self.name),str(self.color),str(self.lowerb),str(self.upperb)])
####

if __name__=="__main__":
	blockFinder = BlockFinder()
	blockFinder.run()
####
