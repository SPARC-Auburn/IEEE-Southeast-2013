
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
		self.createBlockCandidates()

		waitForKeyPress()
		print "DONE!"
	####

	def createBlockCandidates(self):
		(contours,hierarchy) = cv2.findContours( \
								image = self.blockMask.copy(), \
								mode = cv2.RETR_EXTERNAL, \
								method = cv2.CHAIN_APPROX_SIMPLE )

		self.blockCandidates = []
		for contour in contours:
			candidate = BlockCandidate(contour)
			if( (candidate.area > 400) && (candidate.solidarity > 0.75 )):
				blockCandidates.append(candidate)
			####
		####
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
			waitForKeyPress()
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
		return [x[1] for x in area_contours]
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
		showImage("mask coming in...",mask)
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
		contour = biggest_contour

		repaired = []
		hull_cats = []
		for i in range(defects.shape[0]):
			s,e,f,d = defects[i,0]
			start = tuple(contour[s][0])
			end = tuple(contour[e][0])
			far = tuple(contour[f][0])
#			cv2.line(img,start,end,96,2)

#			cv2.circle(img,start,5,200,-1)
#			cv2.circle(img,end,5,200,-1)

#			cv2.circle(img,far,5,128)
#			if( d > 5000):
#				cv2.circle(img,far,7,128)
#				cv2.circle(img,far,9,128)
#			####

			hull_cats.append(contour[s].tolist())
			hull_cats.append(contour[e].tolist())
			if( d > 5000):
				if( e < s):
					repaired.extend(contour[s:].tolist())
					repaired.extend(contour[:(e+1)].tolist())
				else:
					repaired.extend(contour[s:(e+1)].tolist())
				####
			else:
				repaired.append(contour[s].tolist())
				repaired.append(contour[e].tolist())
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
		showImage("mask with hull,repaired,and,biggestcontour",mask)	
		


		print "REPAIRED"
		for (i,ind) in enumerate(repaired):
			print i,ind
		####


		print "\n\nHULL_CATS"
		for (i,t) in enumerate(hull_cats):
			print i,t
		####

		showImage("IMAGE?",img)
		waitForKeyPress()
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

	def colorReduce(self,img,iter=1):
		i = 0xFF;
		for k in xrange(iter):
			img = np.bitwise_and(img,i)
			i = i - 2**k
		####
		return img
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

class BlockCandidate():
	"""This class is just a glorified struct...
	area		  : float 
					moments["m00"]
	contour		  :	np.array, shape = (n,1,2)
	hull		  :	np.array, shape = (n,1)
	defects		  :	np.array, shape = (n,4)
				 			(start_index, end_index,farthest_pt_ind, fixpt_depth)
				 			actual_depth = fixpt_depth/256.0
	solidarity	  :	float
				 		contour_area/hull_area
	moments		  :	dictionairy
	ellipse		  :	rotated rectangle
					((x,y),(width,height),(angle [cw]))
	bounding rect :	rect
					(x,y,width,height)
	center of mass: (x,y)
	mask		  : np.array, shape = (bounding_rect.height,bounding_rect.width),uint8
					the contour is drawn onto the mask
	valid		  : boolean
					=(moments["m00"]>0)
	"""
	def __init__(self,contour):
		self.contour = contour
		print contour.shape[0]
		self.moments = cv2.moments(self.contour)
		self.area = self.moments["m00"]

		if( self.area > 0 ):
			self.valid = True
			self.hull = cv2.convexHull(contour,returnPoints = False)

			self.com	 = (self.moments["m10"]/self.moments["m00"],self.moments["m01"]/self.moments["m00"])
			
			self.solidarity = self.moments["m00"]/cv2.contourArea(self.contour[self.hull.flatten()])

			self.bounding_rect = cv2.boundingRect(self.contour)
			if( self.contour.shape[0]>=5 ):
				self.ellipse = cv2.fitEllipse(self.contour)
				self.defects = cv2.convexityDefects(self.contour,self.hull)
			elif( self.contour.shape[0]>3 ):
				temp = list(self.bounding_rect)
				temp.append(0)
				self.ellipse = tuple(temp)
				self.defects = cv2.convexityDefects(self.contour,self.hull)
			else:
				temp = list(self.bounding_rect)
				temp.append(0)
				self.ellipse = tuple(temp)
				self.defects = np.array([[]])
			####

			self.mask = np.zeros((self.bounding_rect[3],self.bounding_rect[2]),np.uint8)
			shifted_contour = self.contour - (self.bounding_rect[0],self.bounding_rect[1])
			cv2.drawContours( image = self.mask , \
							contours = [shifted_contour], \
							contourIdx = -1, \
							color = (255), \
							thickness = -1 )
		else:
			self.valid = False
		####
	####
	def maskImage(self,img):
		(x,y,w,h) = self.bounding_rect
		view = img[y:y+h,x:x+w]
		return cv2.bitwise_and(view,self.mask)
	####

	def __str__(self):
		out = []
		if( self.valid ):
			out.append("\nCenter Of Mass: ")
			out.append(str(self.com))
			out.append("\nArea: ")
			out.append(str(self.area))
			out.append("\nSolidarity: ")
			out.append(str(self.solidarity))
			out.append("\nBounding Rectangle: ")
			out.append(str(self.bounding_rect))
			out.append("\nMoments:\n")
			out.append(str(self.moments))
		else:
			out.append("Invalid")
		####
		return ''.join(out)
	####

####

def showImage(str,img):
	cv2.namedWindow(str)
	cv2.imshow(str,img)
####

def waitForKeyPress():
	while(1):
		keyPressed = cv2.waitKey(5)

		if( keyPressed == 27 ):
			raise Exception("\n\nQuit on ESC key\n")
		elif( keyPressed != -1 ):
			return keyPressed
		####
	####
####

if __name__=="__main__":
	blockFinder = BlockFinder()
	blockFinder.run()
####
