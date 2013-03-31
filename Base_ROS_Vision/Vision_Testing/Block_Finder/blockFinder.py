
import cv2
import numpy as np
import time
from sys import argv
from os import path,mkdir
from math import sqrt,floor
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
		##Draft#3
		##HSV
		##color = (B,G,R)
		##lower/upperb =(Hue,Sat,Val)
		self.BLACK_YCR_CB_D3 = Threshold( name = "black", \
			color = (0,0,0), \
			lowerb = ( 24, 75,128), \
			upperb = (101,129,144) )
		self.RED_YCR_CB_D3 = Threshold( name = "red", \
			color = (0,0,255), \
			lowerb = (  0,145,109), \
			upperb = ( 82,188,133) )
		self.ORANGE_YCR_CB_D3 = Threshold( name = "orange", \
			color = (0,100,230), \
			lowerb = ( 34,165, 36), \
			upperb = (173,210,107) )
		self.YELLOW_YCR_CB_D3 = Threshold( name = "yellow", \
			color = (0,255,255), \
			lowerb = ( 28,119,  7), \
			upperb = (243,149, 86) )
		self.GREEN_YCR_CB_D3 = Threshold( name = "green", \
			color = (0,255,0), \
			lowerb = ( 16,109, 83), \
			upperb = ( 59,121,253) )
		self.BLUE_YCR_CB_D3 = Threshold( name = "blue", \
			color = (255,0,0), \
			lowerb = (  0, 83,164), \
			upperb = ( 91,135,213) )
		self.BROWN_YCR_CB_D3 = Threshold( name = "brown", \
			color = (0,77,108), \
			lowerb = (  0,129,119), \
			upperb = ( 47,147,130) )
		self.WHITE_YCR_CB_D3 = Threshold( name = "white", \
			color = (255,255,255), \
			lowerb = (238, 44, 77), \
			upperb = (255,132,129) )

		##Draft#2
		##HSV
		##color = (B,G,R)
		##lower/upperb =(Hue,Sat,Val)
		self.BLACK_HSV_D2 = Threshold( name = "black", \
			color = (0,0,0), \
			lowerb = ( 16, 29,130), \
			upperb = (108,194,152) )
		self.RED1_HSV_D2 = Threshold( name = "red1", \
			color = (0,0,255), \
			lowerb = ( 32,147,116), \
			upperb = ( 61,224,155) )
		self.RED2_HSV_D2 = Threshold( name = "red2", \
			color = (0,0,255), \
			lowerb = (231,129, 89), \
			upperb = (159,238,166) )
		self.ORANGE_HSV_D2 = Threshold( name = "orange", \
			color = (0,100,230), \
			lowerb = (  6,154, 47), \
			upperb = (218,222,101) )
		self.YELLOW_HSV_D2 = Threshold( name = "yellow", \
			color = (0,255,255), \
			lowerb = (  0,108,  0), \
			upperb = (255,143,101) )
		self.GREEN_HSV_D2 = Threshold( name = "green", \
			color = (0,255,0), \
			lowerb = (  0,108, 82), \
			upperb = ( 60,123,130) )
		self.BLUE_HSV_D2 = Threshold( name = "blue", \
			color = (255,0,0), \
			lowerb = (  9,  0,154), \
			upperb = ( 78,255,254) )
		self.BROWN_HSV_D2 = Threshold( name = "brown", \
			color = (0,77,108), \
			lowerb = (  6,133, 18), \
			upperb = ( 27,205,236) )

		##YCR_CB
		##color = (B,G,R)
		##lower/upperb =(Y,ChrRed,ChrBlue)
		self.BLACK_YCR_CB_D2 = Threshold( name = "black", \
			color = (0,0,0), \
			lowerb = ( 15, 94,129), \
			upperb = ( 86,130,140) )
		self.RED_YCR_CB_D2 = Threshold( name = "red", \
			color = (0,0,255), \
			lowerb = (  6,139,118), \
			upperb = ( 72,195,126) )
		self.ORANGE_YCR_CB_D2 = Threshold( name = "orange", \
			color = (0,100,230), \
			lowerb = ( 41,154, 44), \
			upperb = (176,202,102) )
		self.YELLOW_YCR_CB_D2 = Threshold( name = "yellow", \
			color = (0,255,255), \
			lowerb = ( 37,122, 14), \
			upperb = (243,141,108) )
		self.GREEN_YCR_CB_D2 = Threshold( name = "green", \
			color = (0,255,0), \
			lowerb = (  3, 98,109), \
			upperb = ( 37,124,130) )
		self.BLUE_YCR_CB_D2 = Threshold( name = "blue", \
			color = (255,0,0), \
			lowerb = (  2, 74,154), \
			upperb = ( 43,143,129) )
		self.BROWN_YCR_CB_D2 = Threshold( name = "brown", \
			color = (0,77,108), \
			lowerb = ( 14,133,127), \
			upperb = ( 43,143,129) )
		####


		###Draft #1
		##HSV
		##color = (B,G,R)
		##lower/upperb =(Hue,Sat,Val)
		self.BLACK_HSV_D1 = Threshold( name = "black", \
								color = (0,0,0), \
								lowerb = (140,  0, 41), \
								upperb = (125, 39, 61) )
		self.RED1_HSV_D1 = Threshold( name = "red1", \
								color = (0,0,255), \
								lowerb = (  0,165, 61), \
								upperb = (  6,212,126) )
		self.RED2_HSV_D1 = Threshold( name = "red2", \
								color = (0,0,255), \
								lowerb = (169,165, 61), \
								upperb = (179,212,126) )
		self.ORANGE_HSV_D1 = Threshold( name = "orange", \
								color = (0,100,230), \
								lowerb = (  4,186,108), \
								upperb = ( 13,255,255) )
		self.YELLOW_HSV_D1 = Threshold( name = "yellow", \
								color = (0,255,255), \
								lowerb = ( 21,148, 97), \
								upperb = ( 32,255,255) )
		self.GREEN_HSV_D1 = Threshold( name = "green", \
								color = (0,255,0), \
								lowerb = ( 54, 74, 44), \
								upperb = ( 78,140, 77) )
		self.BLUE_HSV_D1 = Threshold( name = "blue", \
								color = (255,0,0), \
								lowerb = (108,168, 41), \
								upperb = (121,255,202) )
		self.BROWN_HSV_D1 = Threshold( name = "brown", \
								color = (0,77,108), \
								lowerb = (  2, 74, 51), \
								upperb = ( 15,204, 84) )

		##YCR_CB
		##color = (B,G,R)
		##lower/upperb =(Y,ChrRed,ChrBlue)
		self.BLACK_YCR_CB_D1 = Threshold( name = "black", \
								color = (0,0,0), \
								lowerb = ( 38,127,128), \
								upperb = ( 57,128,133) )
		self.RED_YCR_CB_D1 = Threshold( name = "red", \
								color = (0,0,255), \
								lowerb = ( 31,148,107), \
								upperb = ( 70,177,126) )
		self.ORANGE_YCR_CB_D1 = Threshold( name = "orange", \
								color = (0,100,230), \
								lowerb = ( 49,165, 62), \
								upperb = (162,200,106) )
		self.YELLOW_YCR_CB_D1 = Threshold( name = "yellow", \
								color = (0,255,255), \
								lowerb = ( 78,137, 35), \
								upperb = (239,150, 90) )
		self.GREEN_YCR_CB_D1 = Threshold( name = "green", \
								color = (0,255,0), \
								lowerb = ( 36,110,119), \
								upperb = ( 64,123,128) )
		self.BLUE_YCR_CB_D1 = Threshold( name = "blue", \
								color = (255,0,0), \
								lowerb = ( 18, 85,140), \
								upperb = (117,126,198) )
		self.BROWN_YCR_CB_D1 = Threshold( name = "brown", \
								color = (0,77,108), \
								lowerb = ( 31,138,114), \
								upperb = ( 66,148,125) )
		########

		self.ycrcb_thresholds = [ self.BLACK_YCR_CB_D3, \
			self.RED_YCR_CB_D3, \
			self.ORANGE_YCR_CB_D3, \
			self.YELLOW_YCR_CB_D3, \
			self.GREEN_YCR_CB_D3, \
			self.BLUE_YCR_CB_D3, \
			self.BROWN_YCR_CB_D3 ]

		self.ycrcb_color_thresholds = [ \
			self.RED_YCR_CB_D3, \
			self.ORANGE_YCR_CB_D3, \
			self.YELLOW_YCR_CB_D3, \
			self.GREEN_YCR_CB_D3, \
			self.BLUE_YCR_CB_D3, \
			self.BROWN_YCR_CB_D3 ]

		self.hsv_thresholds = [ self.BLACK_HSV_D2, \
			self.RED1_HSV_D2, \
			self.RED2_HSV_D2, \
			self.ORANGE_HSV_D2, \
			self.YELLOW_HSV_D2, \
			self.GREEN_HSV_D2, \
			self.BLUE_HSV_D2, \
			self.BROWN_HSV_D2 ]
		########

		########
		##Candidate thresholds
		self.MIN_CANDIDATE_AREA = 250
		self.MIN_CANDIDATE_SOLIDARITY = 0.65

		self.DEFECT_ANGLE_DELTA = 45
		########

		########
		self.distance = lambda a,b: sqrt(((a[0]-b[0])**2+(a[1]-b[1])**2))
		self.angleBetweenPlusAndMinus90 = lambda x: x-180*(x/90)+180*(x/180)
		#######

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
		self.prefix = workingdir +"/"
		
		if( self.store_results == 1 ):
			mkdir(self.prefix)
		####

	####

	def run(self):
		try:
			self.createInitialImages()
			self.findInitialMasks()
			(self.majorDir,self.minorDir)=self.findMajorMinorDireciton()

			showImage("Edge Map",self.edgeMap)
			showImage("Block Mask",self.blockMask)
			showImage("Course Mask",self.courseMask)


			initial_candidates = self.createBlockCandidates(self.blockMask)
			print "Initial Candidates: ",initial_candidates.__len__()

			waitForKeyPress()
			final_candidates = self.analyzeBlockCandidates(initial_candidates)

			waitForKeyPress()
			print "DONE!"
		except:
			waitForKeyPress()
			raise
		####
		
	####

	def createBlockCandidates(self,img):
		"""
		Creates block candidates from a mask, and then 
		thresholds based off of self.MIN_CANDIDATE_AREA and self.MIN_CANDIDATE_SOLIDARITY
		and finally sorts based on area
		"""
		(contours,hierarchy) = cv2.findContours( \
								image = img.copy(), \
								mode = cv2.RETR_EXTERNAL, \
								method = cv2.CHAIN_APPROX_SIMPLE )

		blockCandidates = []
		for contour in contours:
			candidate = BlockCandidate(contour)
			if( (candidate.area > self.MIN_CANDIDATE_AREA) and  \
					(candidate.solidarity > self.MIN_CANDIDATE_SOLIDARITY )):
				blockCandidates.append(candidate)
			####
		####
		blockCandidates.sort(key=lambda x: x.area,reverse=True)
		self.displayCandidates(img,blockCandidates)
		return blockCandidates
	####

	def displayCandidates(self,img,candidates):
		canvas = img.copy()
		canvas = cv2.merge((canvas,canvas,canvas))
		t = str(time.time())
		#print t
		for (i,c) in enumerate(candidates):
			shifted_contour = c.contour +(c.bounding_rect[0],c.bounding_rect[1])
			shifted_hull = self.convertIndexedHull2Contour(c.hull,c.contour)
			shifted_hull = shifted_hull + (c.bounding_rect[0],c.bounding_rect[1])
		#	print shifted_hull
			cv2.drawContours( image = canvas, \
				contours = [shifted_contour], \
				contourIdx = -1, \
				color = (255,0,0), \
				thickness = 0, \
				lineType = cv2.CV_AA)
			cv2.drawContours( image = canvas, \
				contours = [shifted_hull], \
				contourIdx = -1, \
				color = (0,255,0), \
				thickness = 0, \
				lineType = cv2.CV_AA)
			for defect in c.defects:
				x = c.contour[defect[0][2]][0][0] + c.bounding_rect[0]
				y = c.contour[defect[0][2]][0][1] + c.bounding_rect[1]
				p = (x,y)
				cv2.circle(canvas,p,2,(0,0,255),thickness=0)
			####
		####
		print ""
		showImage(t,canvas)
	####

	def convertIndexedHull2Contour(self,hull,contour):
		output = contour[hull[0][0]]
		for i in hull[1:]:
			output = np.vstack((output,contour[i[0]]))
		####
		return output
	####

	def analyzeBlockCandidates(self,initial_candidates):
		"""
		Goes through a list of initial candidates and finds the ones that could have multiple
		blocks per candidate. It will call self.separateBlocks on each of the multiple block candidates
		those block will then go through the process again to see if there are still blocks that need to be
		separated from other blocks
		"""
		num = 650
		final_candidates = []	

		round_candidates = initial_candidates
		i = 0
		while( 1 ):
			multiple_blocks = []
			for candidate in (round_candidates):
				if( round(candidate.hull_area/num)>1 and candidate<0.90):
					multiple_blocks.append(candidate)
				else:
					final_candidates.append(candidate)
				####
			####
			print "Round #",i," Final: ",final_candidates.__len__()," Multiples: ",multiple_blocks.__len__()
			if( multiple_blocks.__len__() == 0 ):
				break
			####

			##sepearate blocks and continue separating
			round_candidates = []
			for candidate in multiple_blocks:
				(retVal,splits)=self.separateBlocks(candidate)
				if( retVal == -1):
					final_candidates.append(candidate)
				else:
					round_candidates.extend(splits)
				####
			####
			i+=1
		####
		return final_candidates
	####

	def findMajorMinorDireciton(self):
		bigBlob = cv2.dilate(self.blockMask,np.ones((3,3)),iterations=5)
		(contours,hierarchy) = cv2.findContours( \
							image = bigBlob.copy(), \
							mode = cv2.RETR_EXTERNAL, \
							method = cv2.CHAIN_APPROX_NONE)
		sorted = self.sortContoursByArea(contours)
		biggest = sorted[0]
		e = cv2.fitEllipse(biggest)
		"""
		cv2.ellipse(bigBlob,e,(128),1)
		cv2.drawContours( image = bigBlob, \
			contours = [biggest], \
			contourIdx = -1, \
			color = (90), \
			thickness = 2, \
			lineType = cv2.CV_AA)
		"""
		major = self.angleBetweenPlusAndMinus90(e[2])
		minor = self.angleBetweenPlusAndMinus90(e[2]+major)
		return (major,minor)
	####

	def separateBlocks(self,candidate):

		num_blocks = round(candidate.hull_area/750)
		big_defects = []
		for defect in candidate.defects:
			if( defect[0][3]/256.0 > 7 ):
				big_defects.append(defect)
			####
		####

		if( big_defects.__len__()<=1 ):
			return (-1,candidate)
		elif( big_defects.__len__()==2 ):
			p1 = candidate.contour[big_defects[0][0][2]] [0]
			p1 = (p1[0],p1[1])
			p2 = candidate.contour[big_defects[1][0][2]] [0]
			p2 = (p2[0],p2[1])

			mask = candidate.mask.copy()
			cv2.line(mask,p1,p2,(0),thickness=1)
			cv2.circle(mask,p1,2,(0),thickness=-1)
			cv2.circle(mask,p2,2,(0),thickness=-1)
			split_candidates = self.createBlockCandidates(mask)

			print "EASY SPLIT!!"
			t = str(int(time.time()))
			showImage("Simple Split Candidate:"+t,candidate.maskImage(self.img_ycrcb))
			showImage("Simple-Split Candidate with Line: "+t,mask)

			##fix offset for block children
			offset_x = candidate.bounding_rect[0]
			offset_y = candidate.bounding_rect[1]
			for (i,block) in enumerate(split_candidates):
				temp = list(block.bounding_rect)
				temp[0]+=offset_x
				temp[1]+=offset_y
				block.bounding_rect = temp
			####
			return (1,split_candidates)
		else:	

			cat = candidate.mask.copy()
			########
			##Build mathcing defect pairs
			defect_pairs = {}
			for (i,defect) in enumerate(big_defects):
				defects_copy = list(big_defects)
				defects_copy.pop(i)

				pt1 = candidate.contour[defect[0][0]] [0]
				pt2 = candidate.contour[defect[0][1]] [0]
				farthest = candidate.contour[defect[0][2]] [0]

				point_along_hull = self.findClosestPointAlongLine(pt1,pt2,farthest)

				points = [candidate.contour[x[0][2]][0] for x in defects_copy]
				closest_index = self.findClosestPointToLine(point_along_hull,farthest,points)
				if( closest_index>=i ): #fix the index because defects_copy popped an element
					closest_index+=1
				####
				defect_pairs[i]=closest_index
				
				closest_point = candidate.contour[big_defects[closest_index][0][2]][0]
				cv2.circle(cat,(farthest[0],farthest[1]),5,(0,0,255))
				cv2.line(cat,(farthest[0],farthest[1]),(closest_point[0],closest_point[1]),(0,255,0),thickness=1)
			####

			t = str(time.time())
			showImage("Multi-split: "+t,cat)
			#######
			##Confirm pairs
			points_to_eliminate = set([])
			for (i,j) in defect_pairs.items():
				if( i != defect_pairs[j] ):
					points_to_eliminate.update([i,j])
					k = defect_pairs[j]
					while( k not in points_to_eliminate ):
						points_to_eliminate.add(k)
						k = defect_pairs[k]
					####
				####
			####

			all_points = set(range(big_defects.__len__()))
			valid_points = all_points-points_to_eliminate


			valid_pairs = [ (x,defect_pairs[x]) for x in valid_points]
			for (i,j) in valid_pairs:
				if( (j,i) in valid_pairs):
					valid_pairs.remove((j,i))
				####
			####
			########


			########
			##Draw on mask
			mask = candidate.mask.copy()
			"""
			print "VALID PAIRS"
			print valid_pairs
			"""
			for (i,j) in valid_pairs:
				p1 = candidate.contour[big_defects[i][0][2]] [0]
				p1 = (p1[0],p1[1])
				p2 = candidate.contour[big_defects[j][0][2]] [0]
				p2 = (p2[0],p2[1])

				cv2.line(mask,p1,p2,(0),thickness=2)
				cv2.circle(mask,p1,2,(0),thickness=-1)
				cv2.circle(mask,p2,2,(0),thickness=-1)
			####
			########

			########
			##Create split children
			split_candidates = self.createBlockCandidates(mask)
			print "SPLIT!!"
			t = str(int(time.time()))
			showImage("Multi-Split Candidate:"+t,candidate.maskImage(self.img_ycrcb))
			showImage("Multi-Split Candidate with Line: "+t,mask)

			##fix offset for block children
			offset_x = candidate.bounding_rect[0]
			offset_y = candidate.bounding_rect[1]
			for (i,block) in enumerate(split_candidates):
				temp = list(block.bounding_rect)
				temp[0]+=offset_x
				temp[1]+=offset_y
				block.bounding_rect = temp
			####
			########

			return (1,split_candidates)
		####

		assert False
		return "CATS!!!!"
	####

	def findClosestPointAlongLine(self,pt1,pt2,point):
		v = pt2-pt1
		t = (-1.0*(v*(pt1-point)).sum())/((v**2).sum())
		closest_point = np.int64((v*t+pt1).round())
		return closest_point
	####

	def findClosestPointToLine(self,pt1,pt2,points):
		d=[]				
		v = pt2-pt1
		for point in points:
			t = (-1.0*(v*(pt1-point)).sum())/((v**2).sum())
			d.append(self.distance(v*t+pt1,point))
		####
		return d.index(min(d))
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

	def createInitialImages(self):
		img_med = self.medianFilter(self.original)
		self.img_ycrcb = cv2.cvtColor(img_med,cv2.COLOR_BGR2YCR_CB)
		self.img_hsv   = cv2.cvtColor(img_med,cv2.COLOR_BGR2HSV)
		(h,s,v) = cv2.split(self.img_hsv)

		self.edgeMap = cv2.Canny( image = v, \
							threshold1 = 0, \
							threshold2 = 255, \
							apertureSize = 3, \
							L2gradient = True)
	####

	def findInitialMasks(self):
		thr_black_ycrcb = cv2.inRange(src = self.img_ycrcb, \
								lowerb = self.BLACK_YCR_CB_D2.lowerb, \
								upperb = self.BLACK_YCR_CB_D2.upperb )
		thr_high_sat =    cv2.inRange(src = self.img_hsv, \
								lowerb = np.array((0,85,0),np.uint8), \
								upperb = np.array((255,255,255),np.uint8) )

		thr_colors = np.zeros_like(thr_black_ycrcb)
		for color in self.ycrcb_color_thresholds:
			temp = cv2.inRange(src = self.img_ycrcb, \
						lowerb = color.lowerb, \
						upperb = color.upperb )
			thr_colors = cv2.bitwise_or(thr_colors,temp)
		####
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

		possible_blocks = thr_colors#cv2.bitwise_or(thr_high_sat,thr_colors)
		self.blockMask = cv2.bitwise_and(possible_blocks,self.courseMask)
		self.blockMask = cv2.erode(self.blockMask,np.ones((3,3)),iterations=1)
		self.blockMask = cv2.dilate(self.blockMask,np.ones((3,3)),iterations=2)
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
	contour		  :	np.array, shape = (n,1,2)
	hull		  :	np.array, shape = (n,1)
	area		  : float 
					moments["m00"]
	hull_area	  : float
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
		self.bounding_rect = cv2.boundingRect(contour)
		self.contour = contour - (self.bounding_rect[0],self.bounding_rect[1])
		self.moments = cv2.moments(self.contour)
		self.area = self.moments["m00"]

		if( self.area > 0 ):
			self.valid = True
			self.hull = cv2.convexHull(contour,returnPoints = False)
			self.hull_area = cv2.contourArea(self.contour[self.hull.flatten()])
			self.com	 = (self.moments["m10"]/self.area,self.moments["m01"]/self.area)
			
			self.solidarity = self.area/self.hull_area

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
			cv2.drawContours( image = self.mask , \
							contours = [self.contour], \
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
		depth = view.shape[2]
		if( depth == 3 ):
			temp_mask = cv2.merge((self.mask,self.mask,self.mask))
			return cv2.bitwise_and(view,temp_mask)
		else:
			return cv2.bitwise_and(view,self.mask)
		####
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
