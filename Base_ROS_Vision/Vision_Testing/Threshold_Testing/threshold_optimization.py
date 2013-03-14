
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
		self.red1_hsv = Threshold( name = "red", \
								color = (0,0,255), \
								lowerb = (  0,165, 61), \
								upperb = (  6,212,126) )
		self.red2_hsv = Threshold( name = "red", \
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
		self.workingdir = workingdir+"/optimization_test_images/"

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

		self.SIGMA = 1
		self.N = 20
		self.MAX_ITER = 5000
		self.MIN_FITNESS = 0

	####

	def run(self):

		##Initializations
		ycrcb_img = cv2.cvtColor(self.original,cv2.COLOR_BGR2YCR_CB)
		hsv_img = cv2.cvtColor(self.original,cv2.COLOR_BGR2HSV)
		outputFile = open(self.workingdir+"Threshold_Optimization_Test_"+str(self.curtim)+".txt",'w')

		hsv_list_minus_reds =[ self.black_hsv, \
							self.orange_hsv, \
							self.yellow_hsv, \
							self.green_hsv, \
							self.blue_hsv, \
							self.brown_hsv ]
		try:
			outputFile.write("YCR_CB Optimization\n")

			for initial_seed in self.ycrcb_thresholds:
				iterations = 0
				stale_gen = 0
				seed = initial_seed
				sigma = self.SIGMA
				##Best initializations...
				thr_img = cv2.inRange(src = ycrcb_img, \
										lowerb = seed.lowerb, \
										upperb = seed.upperb )
				best_score = self.findFitness(thr_img,self.correct_id[seed.name])
				best_child = seed
				outputFile.write("\n\nSeed\t"+str(best_score)+"\t"+str(best_child)+"\n")
				while( iterations < self.MAX_ITER and best_score >= self.MIN_FITNESS ):
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

						if( stale_gen > 20 ):
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

			outputFile.write("\n\nHSV Optimization\n")
			
			for initial_seed in hsv_list_minus_reds:
				iterations = 0
				stale_gen = 0
				seed = initial_seed
				sigma = self.SIGMA
				##Best initializations...
				thr_img = cv2.inRange(src = ycrcb_img, \
										lowerb = seed.lowerb, \
										upperb = seed.upperb )
				best_score = self.findFitness(thr_img,self.correct_id[seed.name])
				best_child = seed
				outputFile.write("\n\nSeed\t"+str(best_score)+"\t"+str(best_child)+"\n")
				while( iterations < self.MAX_ITER and best_score >= self.MIN_FITNESS ):
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

						if( stale_gen > 20 ):
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
			
			###THE STUPID RED OPTIMIZATION BECAUSE STUPID HUE IS CONTINUOUS LIKE ANGLES< SO RED NEEDS TO BE SPECIAL> UGH>>>>

			
			iterations = 0
			stale_gen = 0
			seed1 = self.red1_hsv
			seed2 = self.red2_hsv
			sigma = self.SIGMA
			##Best initializations...
			thr_img1 = cv2.inRange(src = ycrcb_img, \
									lowerb = seed1.lowerb, \
									upperb = seed1.upperb )
			thr_img2 = cv2.inRange(src = ycrcb_img, \
									lowerb = seed2.lowerb, \
									upperb = seed2.upperb )
			thr_img = cv2.bitwise_or(thr_img1,thr_img2)
			best_score = self.findFitness(thr_img,self.correct_id[seed1.name])
			best_child1 = seed1
			best_child2 = seed2
			outputFile.write("\n\nSeed\t"+str(best_score)+"\t"+str(best_child1)+str(best_child2)+"\n")
			while( iterations < self.MAX_ITER and best_score >= self.MIN_FITNESS ):
				children1 = self.generateThresholdValues(seed1,sigma)
				children2 = self.generateThresholdValues(seed2,sigma)
				fitness_scores = []
				for (i,(child1,child2)) in enumerate(zip(children1,children2)):
					thr_img1 = cv2.inRange(src = ycrcb_img, \
											lowerb = child1.lowerb, \
											upperb = child1.upperb )
					thr_img2 = cv2.inRange(src = ycrcb_img, \
											lowerb = child2.lowerb, \
											upperb = child2.upperb )
					thr_img = cv2.bitwise_or(thr_img1,thr_img2)
					fitness = self.findFitness(thr_img,self.correct_id[child1.name])
					fitness_scores.append( (fitness,i) )
				####
				(gen_score,index) = min(fitness_scores)
				iterations = iterations +1

				if( gen_score < best_score ):
					best_score = gen_score
					best_child1 = seed1
					best_child2 = seed2
					seed1 = children1[index]
					seed2 = children2[index]
					stale_gen = 0
					outputFile.write(str(iterations)+"\t"+str(gen_score)+"\t"+str(seed1)+str(seed2)+"\n")
				else:
					stale_gen = stale_gen + 1

					if( stale_gen > 20 ):
						sigma = sigma + 1
						outputFile.write("Stale generation:\t"+str(iterations)+"\tsigma: "+str(sigma)+"\n")
						stale_gen = 0
					####					
				####
				if( self.watch == True ):
					cv2.waitKey(100)
				####
			####
			outputFile.write("BEST!\nscore: "+str(best_score)+"\tthreshold: "+str(best_child1)+str(best_child2)+"\n")
			
			
			
			


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
