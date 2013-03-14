
import cv2
import numpy as np
import time
from sys import argv
from os import path,mkdir
from random import gauss
"""

This python program is a branch from threshold_2

This is meant to optimize the threshold values
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

		###Draft #1
		##HSV
		##color = (B,G,R)
		##lower/upperb =(Hue,Sat,Val)
		self.black_hsv = Threshold( name = "black", \
								color = (0,0,0), \
								lowerb = (140,  0, 41), \
								upperb = (125, 39, 61) )
		self.red1_hsv = Threshold( name = "red1", \
								color = (0,0,255), \
								lowerb = (  0,165, 61), \
								upperb = (  6,212,126) )
		self.red2_hsv = Threshold( name = "red2", \
								color = (0,0,255), \
								lowerb = (169,165, 61), \
								upperb = (179,212,126) )
		self.orange_hsv = Threshold( name = "orange", \
								color = (0,100,230), \
								lowerb = (  4,186,108), \
								upperb = ( 13,255,255) )
		self.yellow_hsv = Threshold( name = "yellow", \
								color = (0,255,255), \
								lowerb = ( 21,148, 97), \
								upperb = ( 32,255,255) )
		self.green_hsv = Threshold( name = "green", \
								color = (0,255,0), \
								lowerb = ( 54, 74, 44), \
								upperb = ( 78,140, 77) )
		self.blue_hsv = Threshold( name = "blue", \
								color = (255,0,0), \
								lowerb = (108,168, 41), \
								upperb = (121,255,202) )
		self.brown_hsv = Threshold( name = "brown", \
								color = (0,77,108), \
								lowerb = (  2, 74, 51), \
								upperb = ( 15,204, 84) )

		self.hsv_thresholds = [ self.black_hsv, \
							self.red1_hsv, \
							self.red2_hsv, \
							self.orange_hsv, \
							self.yellow_hsv, \
							self.green_hsv, \
							self.blue_hsv, \
							self.brown_hsv ]
		##YCR_CB
		##color = (B,G,R)
		##lower/upperb =(Y,ChrRed,ChrBlue)
		self.black_ycrcb = Threshold( name = "black", \
								color = (0,0,0), \
								lowerb = ( 38,127,128), \
								upperb = ( 57,128,133) )
		self.red_ycrcb = Threshold( name = "red", \
								color = (0,0,255), \
								lowerb = ( 31,148,107), \
								upperb = ( 70,177,126) )
		self.orange_ycrcb = Threshold( name = "orange", \
								color = (0,100,230), \
								lowerb = ( 49,165, 62), \
								upperb = (162,200,106) )
		self.yellow_ycrcb = Threshold( name = "yellow", \
								color = (0,255,255), \
								lowerb = ( 78,137, 35), \
								upperb = (239,150, 90) )
		self.green_ycrcb = Threshold( name = "green", \
								color = (0,255,0), \
								lowerb = ( 36,110,119), \
								upperb = ( 64,123,128) )
		self.blue_ycrcb = Threshold( name = "blue", \
								color = (255,0,0), \
								lowerb = ( 18, 85,140), \
								upperb = (117,126,198) )
		self.brown_ycrcb = Threshold( name = "brown", \
								color = (0,77,108), \
								lowerb = ( 31,138,114), \
								upperb = ( 66,148,125) )

		self.ycrcb_thresholds = [ self.black_ycrcb, \
							self.red_ycrcb, \
							self.orange_ycrcb, \
							self.yellow_ycrcb, \
							self.green_ycrcb, \
							self.blue_ycrcb, \
							self.brown_ycrcb ]
		########

		(workingdir,exec_ext) = path.split(path.realpath(__file__))
		self.curtim = int(time.time())
		self.workingdir = workingdir+"/"

		self.original = cv2.imread(self.workingdir+"original.png")

		self.correct_id = { \
			"black": cv2.imread(self.workingdir+"black.png",cv2.CV_LOAD_IMAGE_GRAYSCALE), \
			"red": cv2.imread(self.workingdir+"red.png",cv2.CV_LOAD_IMAGE_GRAYSCALE), \
			"orange": cv2.imread(self.workingdir+"orange.png",cv2.CV_LOAD_IMAGE_GRAYSCALE), \
			"yellow": cv2.imread(self.workingdir+"yellow.png",cv2.CV_LOAD_IMAGE_GRAYSCALE), \
			"green": cv2.imread(self.workingdir+"green.png",cv2.CV_LOAD_IMAGE_GRAYSCALE), \
			"blue":	cv2.imread(self.workingdir+"blue.png",cv2.CV_LOAD_IMAGE_GRAYSCALE), \
			"brown": cv2.imread(self.workingdir+"brown.png",cv2.CV_LOAD_IMAGE_GRAYSCALE) }

		self.watch = False

		self.SIGMA = 8
		self.N = 150
		self.MAX_ITER = 5000
		self.MIN_FITNESS = 0

	####

	def run(self):

		##Initializations
		ycrcb_img = cv2.cvtColor(self.original,cv2.COLOR_BGR2YCR_CB)
		outputFile = open(self.workingdir+"Threshold_Optimization_Test_"+str(self.curtim)+".txt",'w')
		try:
			for initial_seed in self.ycrcb_thresholds:
				iterations = 0
				stale_gen = 0
				seed = initial_seed

				##Best initializations...
				thr_img = cv2.inRange(src = ycrcb_img, \
										lowerb = seed.lowerb, \
										upperb = seed.upperb )
				best_score = self.findFitness(thr_img,self.correct_id[seed.name])
				best_child = seed
				outputFile.write("\n\nSeed\t"+str(best_score)+"\t"+str(best_child))
				while( iterations < self.MAX_ITER and best_score >= self.MIN_FITNESS ):
					children = self.generateThresholdValues(seed)
					fitness_scores = []
					for (i,child) in enumerate(children):
						thr_img = cv2.inRange(src = ycrcb_img, \
												lowerb = child.lowerb, \
												upperb = child.upperb )
						fitness = self.findFitness(thr_img,self.correct_id[child.name])
						fitness_scores.append( (fitness,i) )
					####
					(gen_score,index) = min(fitness_scores)
					iterations = iterations +1

					if( gen_score < best_score ):
						best_score = gen_score
						best_child = seed
						seed = children[index]
						stale_gen = 0
						outputFile.write(str(iterations)+"\t"+str(gen_score)+"\t"+str(seed))
					else:
						stale_gen = stale_gen + 1

						if( stale_gen > 20 ):
							self.SIGMA = self.SIGMA + 1
							outputFile.write("Stale generation:\t"+str(i)+"\tsigma: "+str(self.SIGMA))
							stale_gen = 0
						####					
					####
					if( self.watch == True ):
						cv2.waitKey(100)
					####
				####
				outputFile.write("\nBEST!\nscore: "+str(best_score)+"\tthreshold: "+str(best_child))
			####
		except:
			outputFile.close()
			raise
		####
		outputFile.close()
	####

	def generateThresholdValues(self,seed):
		"""
		Takes in a Threshold object and generates N similar Threshold objects
		"""
		children = []
		for i in xrange(self.N):

			lowerb = self.random_thresh(seed.lowerb)
			upperb = self.random_thresh(seed.upperb)
			children.append( Threshold( seed.name,seed.color,lowerb,upperb))
		####
		return children
	####

	def random_thresh(self,t):
		tmp = t+np.array([gauss(0,self.SIGMA),gauss(0,self.SIGMA),gauss(0,self.SIGMA)])
		tmp[tmp>255]=255
		tmp[tmp<0]=0
		return np.array(tmp,np.uint8)
	####

	def sat_add(self,array,scalar):
		tmp = np.array(array,np.float64)
		tmp = tmp+scalar
		tmp[tmp>255]=255
		tmp[tmp<0]=0
		return np.array(tmp,np.uint8)
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

	def findFitness(self,im1,im2):
		t = cv2.absdiff(im1,im2)
		if( self.watch == True ):
			cv2.imshow("cats",t)
			cv2.waitKey(50)
		####
		return t.sum()
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
