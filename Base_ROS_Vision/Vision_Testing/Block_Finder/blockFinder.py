
import cv2
import numpy as np
import time
from sys import argv
from os import path,mkdir
from math import sqrt,floor,atan,pi,atan2
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
		########


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
		########


		########
		##Candidate thresholds
		self.MIN_CANDIDATE_AREA = 250
		self.MIN_CANDIDATE_SOLIDARITY = 0.65

		self.DEFECT_ANGLE_DELTA = 50
		self.DEFECT_FARTHEST_THRESHOLD = 2.0

		self.majorDir = 0
		self.minorDir = 90
		########


		########
		##Lambdas because these formulas are annoying
		self.distance = lambda a,b: sqrt(((a[0]-b[0])**2+(a[1]-b[1])**2))
		self.angleBetweenPlusAndMinus90 = lambda x: x-180*floor(x/90)+180*floor(x/180)
		self.angleBetweenPoints = lambda a,b: atan(1.0*(b[1]-a[1])/(b[0]-a[0]))*180/pi
		self.validMinorLine = lambda a,b: (abs(self.angleBetweenPoints(a,b)-self.minorDir)<self.DEFECT_ANGLE_DELTA)
		########


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


		########
		(workingdir,exec_ext) = path.split(path.realpath(__file__))
		self.curtim = int(time.time())
		self.prefix = workingdir +"/"
		
		if( self.store_results == 1 ):
			mkdir(self.prefix)
		####
		########
	####

	def run(self):
		try:
			self.createInitialImages()
			self.findInitialMasks()
			(self.majorDir,self.minorDir)=self.findMajorMinorDireciton()

			print "Major direciton: ",self.majorDir
			print "Minor direciton: ",self.minorDir
			showImage("Edge Map",self.edgeMap)
			showImage("Block Mask",self.blockMask)
			showImage("Course Mask",self.courseMask)


			initial_candidates = self.createBlockCandidates(self.blockMask)
			print "Initial Candidates: ",initial_candidates.__len__()
			self.displayCandidates(self.blockMask,(0,0),initial_candidates)

			waitForKeyPress()
			final_candidates = self.analyzeBlockCandidates(initial_candidates)

			waitForKeyPress()
			print "DONE!"
		except:
			waitForKeyPress()
			raise
		####
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
								lowerb = self.BLACK_YCR_CB_D3.lowerb, \
								upperb = self.BLACK_YCR_CB_D3.upperb )
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
	
	def findMajorMinorDireciton(self):
		bigBlob = cv2.dilate(self.blockMask,np.ones((3,3)),iterations=5)
		(contours,hierarchy) = cv2.findContours( \
							image = bigBlob.copy(), \
							mode = cv2.RETR_EXTERNAL, \
							method = cv2.CHAIN_APPROX_NONE)
		sorted = self.sortContoursByArea(contours)
		biggest = sorted[0]
		e = cv2.fitEllipse(biggest)

#		cv2.ellipse(bigBlob,e,(128),1)
#		cv2.drawContours( image = bigBlob, \
#			contours = [biggest], \
#			contourIdx = -1, \
#			color = (90), \
#			thickness = 2, \
#			lineType = cv2.CV_AA)
		print e
		if( e[1][1] > e[1][0] ): ##height > width
			minor = self.angleBetweenPlusAndMinus90(e[2])
			major = self.angleBetweenPlusAndMinus90(minor+90)
		else:					 ##width  > height
			major = self.angleBetweenPlusAndMinus90(e[2])
			minor = self.angleBetweenPlusAndMinus90(minor+90)
		####
		return (major,minor)
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
		for (i,c) in enumerate(blockCandidates):
			c.id = str(i)
		####
		return blockCandidates
	####

	def displayCandidates(self,img,imgoffset,candidates):
		canvas = img.copy()
		canvas = cv2.merge((canvas,canvas,canvas))
		t = str(time.time())
		u = ''
		#print t
		for (i,c) in enumerate(candidates):
			offset = (c.x-imgoffset[0],c.y-imgoffset[1])
#			offset = (c.boundingRect[0]-imgoffset[0],c.boundingRect[1]-imgoffset[1])			
			shifted_contour = c.contour + offset

			shifted_hull = self.convertIndexedHull2Contour(c.hull,c.contour)
			shifted_hull = shifted_hull + offset
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

			##DEFECTS
			for defect in c.defects:
				x = c.contour[defect[0][2]][0][0] + offset[0]
				y = c.contour[defect[0][2]][0][1] + offset[1]
				p = (x,y)
				cv2.circle(canvas,p,2,(0,0,255),thickness=0)
			####

			for defect in c.defects:
				pt1 = c.contour[defect[0][0]] [0]
				pt2 = c.contour[defect[0][1]] [0]
				f = c.contour[defect[0][2]] [0] #farthest point from hull
				
				#point along hull line closest to the farthest point
				pth = self.findClosestPointAlongLine(pt1,pt2,f)
				f = (f[0]+offset[0],f[1]+offset[1])
				pth = (pth[0]+offset[0],pth[1]+offset[1])
				cv2.line(canvas,pth,f,(255,0,255),0,cv2.CV_AA)
			####

			for defect in self.filterDefects(c):
				x = defect[2][0] + offset[0]
				y = defect[2][1] + offset[1]
				p = (x,y)
				cv2.circle(canvas,p,3,(0,0,255),thickness=0)
			####
			u = u+c.id+","
		####
		u = u[0:-1]
		showImage(u,canvas)
	####

	def analyzeBlockCandidates(self,initial_candidates):
		"""
		Goes through a list of initial candidates and finds the ones that could have multiple
		blocks per candidate. It will call self.separateBlocks on each of the multiple block candidates
		those block will then go through the process again to see if there are still blocks that need to be
		separated from other blocks
		"""
		num = 250
		final_candidates = []	

		round_candidates = initial_candidates
		i = 0
		while( 1 ):
			multiple_blocks = []
			for candidate in (round_candidates):
				print candidate.id," ",candidate.x,candidate.y,candidate.w,candidate.h
				if( round(candidate.hull_area/num)>1 and candidate<0.90):
					multiple_blocks.append(candidate)
				else:
					print "Candidate: ",candidate.id," finalized because..."
					print "\tPoss. blocks inside ==",round(candidate.hull_area/num)
					print "\tSolidatiry ==",candidate.solidarity
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
					print "Candidate: ",candidate.id," finalized because..."
					print "\tCould not split any further"
					final_candidates.append(candidate)
				else:
					round_candidates.extend(splits)
				####
			####
			i+=1
			waitForKeyPress()
		####
		return final_candidates
	####

	def filterDefects(self,candidate):
		"""The candidates.defects come in as indices of contour which is a pain...
		so, the filtered are [defect,defect,...]
		where defect = (array(x,y), array(x,y), array(x,y), float)
		"""
		filtered = []
		defects = [(candidate.contour[x[0][0]][0],candidate.contour[x[0][1]][0], \
				candidate.contour[x[0][2]][0],x[0][3]/256.0) for x in candidate.defects]
		print candidate.id
		for defect in defects:
			pt1 = defect[0]
			pt2 = defect[1]
			f = defect[2]#farthest point from hull

			#point along hull line closest to the farthest point
			pth = self.findClosestPointAlongLine(pt1,pt2,f)
			if( defect[3] > self.DEFECT_FARTHEST_THRESHOLD and \
				self.validMinorLine(f,pth) ):

				filtered.append(defect)
			####
			print defect,"\t",self.angleBetweenPoints(f,pth),"\t",self.validMinorLine(f,pth)
		####

		return filtered
	####

	def buildMatchingDefects(self,candidate,defects):
		defect_pairs = {}

		##Find the defect-farthest-points that is closest
		## to the normal line from the current-farthest-point to the hull
		## and is the pairing is a valid minor line
		## for all the defect points
		for (i,defect) in enumerate(defects):
			defects_copy = list(defects)
			defects_copy.pop(i)

			pt1 = defect[0] #candidate.contour[defect[0][0]] [0]
			pt2 = defect[1] #candidate.contour[defect[0][1]] [0]
			farthest = defect[2] #candidate.contour[defect[0][2]] [0]

			point_along_hull = self.findClosestPointAlongLine(pt1,pt2,farthest)

			points = [x[2] for x in defects_copy]
			while( 1 ):
				closest_index = self.findClosestPointToLine(point_along_hull,farthest,points)
				if( self.validMinorLine(farthest,points[closest_index]) ):
					defect_pairs[tuple(farthest)] = tuple(points[closest_index])
					break
				####

				points.pop(closest_index)
				if( points.__len__() == 0):
					break
				####
			####

		####
		########

		##Only keep the pairs that point to themselves
		connected_pairs = [] 
		print "FREAKING DEFECT PAIRS"
		print candidate.id
		print defect_pairs
		for (i,j) in defect_pairs.items():
			if( i == defect_pairs[j] and \
				(i,j) not in connected_pairs and \
				(j,i) not in connected_pairs):
				connected_pairs.append((i,j))
			####
		####
		print "FREAKING CONNECTED PAIRS"
		print connected_pairs

		##Eliminate points that do not point along the minorDir
#		valid_pairs = []
#		print ""
#		print "Buliding defect pairs for ",candidate.id
#		for (i,j) in connected_pairs:
#			d1 = candidate.contour[filteredDefects[i][0][2]] [0]
#			d2 = candidate.contour[filteredDefects[j][0][2]] [0]
#
#			if( self.validMinorLine(d1,d2) ):
#				valid_pairs.append((i,j))
#			####
#			print d2,"\t",d1,"\t",self.angleBetweenPoints(d1,d2),"\t",self.validMinorLine(d1,d2)
#		####
#		print "done building defect pairs."

		##Convert defect indices into x,y points
		valid_points = connected_pairs
#		valid_points = [(filteredDefects[i][0][2],filteredDefects[j][0][2]) \
#					for (i,j) in valid_pairs]

		return valid_points
	####

	def drawOnMask(self,candidate,pairs):
		mask = candidate.mask.copy()
		print pairs
		for (p1,p2) in pairs:
			p1 = (p1[0],p1[1])
			p2 = (p2[0],p2[1])

			cv2.line(mask,p1,p2,(0),thickness=2)
			cv2.circle(mask,p1,2,(0),thickness=-1)
			cv2.circle(mask,p2,2,(0),thickness=-1)
		####
		return mask
	####

	def updateChildren(self,children,candidate):
		##fix offset for block children
		for (i,block) in enumerate(children):
			block.x += candidate.x
			block.y += candidate.y
			block.id = candidate.id + ":" + block.id
		####
		return 1
	####
	
	def separateBlocks(self,candidate):

		num_blocks = round(candidate.hull_area/750)
		defects = self.filterDefects(candidate)

		if( defects.__len__()<=1 ):
			return (-1,candidate)		
		elif( defects.__len__()==2 ):

			pairs = [(defects[0][2],defects[1][2])]
			mask = self.drawOnMask(candidate,pairs)
			splitCandidates = self.createBlockCandidates(mask)

			self.updateChildren(splitCandidates,candidate)
			offset = (candidate.x,candidate.y)
			self.displayCandidates(mask,offset,splitCandidates)
			return (1,splitCandidates)
		else:	

			pairs = self.buildMatchingDefects(candidate,defects)
			mask = self.drawOnMask(candidate,pairs)
			splitCandidates = self.createBlockCandidates(mask)
			self.updateChildren(splitCandidates,candidate)

			offset = (candidate.x,candidate.y)
			self.displayCandidates(mask,offset,splitCandidates)
			return (1,splitCandidates)
		####

		assert False
		return "CATS!!!!"
	####
	
	"""
	This next section is for general functions
	that are used more than once and in multiple locations
	"""

	def sortContoursByArea(self,contours):
		area_contours = []
		for contour in contours:
			area_contours.append((cv2.contourArea(contour),contour))
		####
		area_contours.sort(key=lambda x: x[0],reverse = True)
		return [x[1] for x in area_contours]
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
	
	def convertIndexedHull2Contour(self,hull,contour):
		output = contour[hull[0][0]]
		for i in hull[1:]:
			output = np.vstack((output,contour[i[0]]))
		####
		return output
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
	id			  : identifier, 
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
	(x,y,w,h)     : bounding rect 
	center of mass: (x,y)
	mask		  : np.array, shape = (boundingRect.height,boundingRect.width),uint8
					the contour is drawn onto the mask
	valid		  : boolean
					=(moments["m00"]>0)
	"""
	def __init__(self,contour):
		self.id = id
		boundingRect = cv2.boundingRect(contour)
		self.x = boundingRect[0]-1
		self.y = boundingRect[1]-1
		self.w = boundingRect[2]+1
		self.h = boundingRect[3]+1
		self.contour = contour - (self.x,self.y)
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
				temp = list(self.boundingRect)
				temp.append(0)
				self.ellipse = tuple(temp)
				self.defects = cv2.convexityDefects(self.contour,self.hull)
			else:
				self.ellipse = (self.x,self.y,self.w,self.h,0)
				self.defects = np.array([[]])
			####

			self.mask = np.zeros((self.h+1,self.w+1),np.uint8)
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
		view = img[self.y : self.y+self.h, self.x : self.x+self.w]
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
			out.append(str(self.boundingRect))
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
