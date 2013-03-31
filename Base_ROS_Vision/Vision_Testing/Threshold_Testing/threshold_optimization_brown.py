
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

		##YCR_CB
		##color = (B,G,R)
		##lower/upperb =(Y,ChrRed,ChrBlue)

		##color = (B,G,R)
		##lower/upperb =(Y,ChrRed,ChrBlue)
		self.BLACK_YCR_CB_D3 = Threshold( name = "black", \
			color = (0,0,0), \
			lowerb = ( 24, 75,128), \
			upperb = (101,129,144) )
		self.RED_YCR_CB_D3 = Threshold( name = "red", \
			color = (0,0,255), \
			lowerb = (  6,139,118), \
			upperb = ( 72,195,126) )
		self.ORANGE_YCR_CB_D3 = Threshold( name = "orange", \
			color = (0,100,230), \
			lowerb = ( 37,163, 37), \
			upperb = (174,210,108) )
		self.YELLOW_YCR_CB_D3 = Threshold( name = "yellow", \
			color = (0,255,255), \
			lowerb = ( 29,120,  8), \
			upperb = (242,148, 86) )
		self.GREEN_YCR_CB_D3 = Threshold( name = "green", \
			color = (0,255,0), \
			lowerb = (  0, 83,164), \
			upperb = ( 91,135,213) )
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
			lowerb = (237, 45, 78), \
			upperb = (255,132,129) )
		####

		self.ycrcb_thresholds = [#self.BLACK_YCR_CB_D3, \
						#		self.RED_YCR_CB_D3, \
						#		self.ORANGE_YCR_CB_D3, \
						#		self.YELLOW_YCR_CB_D3, \
						#		self.GREEN_YCR_CB_D3, \
						#		self.BLUE_YCR_CB_D3,  \
								self.BROWN_YCR_CB_D3, \
						#		self.WHITE_YCR_CB_D3 
						]
		########

		(workingdir,exec_ext) = path.split(path.realpath(__file__))
		self.curtim = int(time.time())
		self.workingdir = workingdir+"/optimization_test_images_brown/"

		self.original = cv2.imread(self.workingdir+"original.png")

		self.correct_id = { \
			"black": cv2.imread(self.workingdir+"black.png",cv2.CV_LOAD_IMAGE_GRAYSCALE), \
			"red": cv2.imread(self.workingdir+"red.png",cv2.CV_LOAD_IMAGE_GRAYSCALE), \
			"orange": cv2.imread(self.workingdir+"orange.png",cv2.CV_LOAD_IMAGE_GRAYSCALE), \
			"yellow": cv2.imread(self.workingdir+"yellow.png",cv2.CV_LOAD_IMAGE_GRAYSCALE), \
			"green": cv2.imread(self.workingdir+"green.png",cv2.CV_LOAD_IMAGE_GRAYSCALE), \
			"blue":	cv2.imread(self.workingdir+"blue.png",cv2.CV_LOAD_IMAGE_GRAYSCALE), \
			"brown": cv2.imread(self.workingdir+"brown.png",cv2.CV_LOAD_IMAGE_GRAYSCALE), \
			"white": cv2.imread(self.workingdir+"white.png",cv2.CV_LOAD_IMAGE_GRAYSCALE) }

		self.watch = True

		self.SIGMA = .75
		self.N = 400
		self.MAX_ITER = 2000
		self.MIN_FITNESS = 0

	####

	def run(self):

		##Initializations
		ycrcb_img = cv2.cvtColor(self.original,cv2.COLOR_BGR2YCR_CB)
		hsv_img = cv2.cvtColor(self.original,cv2.COLOR_BGR2HSV)
		outputFile = open(self.workingdir+"Threshold_Optimization_Test_"+str(self.curtim)+".txt",'w')
		try:
			outputFile.write("YCR_CB Optimization\n")

			for initial_seed in self.ycrcb_thresholds:
				iterations = 0
				stale_gen = 0
				seed = initial_seed
				sigma = self.SIGMA
				print seed.name
				##Best initializations...
				thr_img = cv2.inRange(src = ycrcb_img, \
										lowerb = seed.lowerb, \
										upperb = seed.upperb )
				best_score = self.findFitness(thr_img,self.correct_id[seed.name])
				best_child = seed
				outputFile.write("\n\nSeed\t"+str(best_score)+"\t"+str(best_child)+"\n")
				k=0
				while( iterations < self.MAX_ITER and best_score >= self.MIN_FITNESS ):
					k+=1
					children = self.generateThresholdValues(seed,sigma)
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
						outputFile.write(str(iterations)+"\t"+str(gen_score)+"\t"+str(seed)+"\n")
					else:
						stale_gen = stale_gen + 1

						if( stale_gen > 100 ):
							sigma = sigma + 1
							outputFile.write("Stale generation:\t"+str(iterations)+"\tsigma: "+str(sigma)+"\n")
							stale_gen = 0
						####					
					####
					if( self.watch == True ):
						cv2.waitKey(100)
					####
				####
				outputFile.write("BEST!\nscore: "+str(best_score)+"\tthreshold: "+str(best_child)+"\n")
			####

			
		except:
			outputFile.close()
			raise
		####
		outputFile.close()
	####

	def generateThresholdValues(self,seed,sigma):
		"""
		Takes in a Threshold object and generates N similar Threshold objects
		"""
		children = []
		for i in xrange(self.N):

			lowerb = self.random_thresh(seed.lowerb,sigma)
			upperb = self.random_thresh(seed.upperb,sigma)
			children.append( Threshold( seed.name,seed.color,lowerb,upperb))
		####
		return children
	####

	def random_thresh(self,t,sigma):
		tmp = t+np.array([gauss(0,sigma),gauss(0,sigma),gauss(0,sigma)])
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
