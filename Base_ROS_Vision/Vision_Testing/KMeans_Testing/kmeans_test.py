
import numpy as np
import cv2
from os import path

"""Note!
kmeans will only take dtype=np.float32. SOLAMENTE!
"""

def waitForKeyPress():
	while( 1 ):
		keyPressed = cv2.waitKey(10)
		if( keyPressed == 27 ):
			assert False
		elif( keyPressed != -1 ):
			return keyPressed
		####
	####
####

def main():
	
	(workingdir,exec_ext) = path.split(path.realpath(__file__))
	prefix = workingdir + "/"
	img = cv2.imread(prefix+"../Threshold_Testing/optimization_test_images/blue.png",cv2.CV_LOAD_IMAGE_GRAYSCALE) 
	(height,width) = img.shape
	canvas = np.zeros((height,width,3),np.uint8)

	yx = np.transpose(np.nonzero(img == 255))
	yx = np.float32(yx)

	# Define criteria = ( type, max_iter = 10 , epsilon = 1.0 )
	crit = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
	(retVal,bestLabels,centers) = cv2.kmeans( data = yx, \
											K=6, \
											criteria=crit,\
											attempts=10, \
											flags=cv2.KMEANS_RANDOM_CENTERS)
	colors = {0:(0,0,255),1:(0,255,0),2:(255,0,0),3:(0,255,255),4:(255,255,0),5:(255,0,255)}
	print bestLabels
	print bestLabels.shape
	print "centers"
	print centers
	print centers.shape
	labels = bestLabels.flatten()

	print "\n\n cats:\ncanvas shape"
	print canvas.shape
	print "\n\n"
	for (label,index) in zip(labels,yx):
		y = int(index[0])
		x = int(index[1])
		canvas[y,x,:]=colors[label]
	####
	cv2.namedWindow("cats")
	cv2.imshow("cats",canvas)
	cv2.imwrite(prefix+"KMEANS_blue_test.png",canvas)
	waitForKeyPress()
####

if __name__=="__main__":
	main()
####
