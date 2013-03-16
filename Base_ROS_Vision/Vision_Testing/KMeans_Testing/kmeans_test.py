
import numpy as np
import cv2
from os import path

"""Note!
kmeans will only take dtype=np.float32. ¡SOLAMENTE!
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

	cats = np.array(img,np.float32)

	print cats.ndim
	print cats.dtype
	(retVal,bestLabels,centers) = cv2.kmeans( data = cats, \
											K=6, \
											criteria=(cv2.TERM_CRITERIA_EPS,100,10),\
											attempts=10,	flags=cv2.KMEANS_PP_CENTERS)
	print retVal
	print bestLabels
	print centers
	waitForKeyPress()
####

if __name__=="__main__":
	main()
####
