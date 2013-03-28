
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
	img = cv2.imread(prefix+"../Threshold_Testing/optimization_test_images/orange.png",cv2.CV_LOAD_IMAGE_GRAYSCALE) 

	img = cv2.GaussianBlur(img,(3,3),100)
	(retval,img) = cv2.threshold(img,128,255,cv2.THRESH_BINARY)
	(height,width) = img.shape
	canvas = np.zeros((height,width,3),np.uint8)

	yx = np.transpose(np.nonzero(img == 255))
	yx = np.float32(yx)
	K = 12
	# Define criteria = ( type, max_iter = 10 , epsilon = 1.0 )
	crit = (cv2.TERM_CRITERIA_EPS, 1000, 1)
	(retVal,bestLabels,centers) = cv2.kmeans( data = yx, \
											K=K, \
											criteria=crit,\
											attempts=50, \
											flags=cv2.KMEANS_PP_CENTERS)
	colors = {}
	for i in xrange(K):
		h = np.random.randint(0,179)
		hsv = np.array([[(h,255,255)]],np.uint8)
		colors[i] = cv2.cvtColor(hsv,cv2.COLOR_HSV2BGR)
	####
#	colors = {0:(0,0,255),1:(0,255,0),2:(255,0,0),3:(0,255,255),4:(255,255,0),5:(255,0,255)}
	print bestLabels
	print bestLabels.shape
	print "centers"
	print centers
	print centers.shape
#	labels = bestLabels.flatten()

	print "\n\n cats:\ncanvas shape"
	print canvas.shape
	print "\n\n"
	for (label,index) in zip(bestLabels,yx):
		y = int(index[0])
		x = int(index[1])
		canvas[y,x,:]=colors[label[0]]
	####
	for (i,center) in enumerate(centers):
		y = center[0]
		x = center[1]
		cv2.putText( img = canvas, \
					text = str(i), \
					org = (x,y), \
					fontFace = cv2.FONT_HERSHEY_SIMPLEX, \
					fontScale = 0.5, \
					color = (255,255,255), \
					thickness = 1)
	####

	"""
	for (i,center) in enumerate(centers):
		y = center[0]
		x = center[1]
		for j in xrange(5,0,-1):
			cv2.circle(canvas,(x,y),2*j+1,color=(255-j*10,255-j*10,255-j*10))
		####
	####

	(contours,hierarcy) = cv2.findContours( \
							image = img, \
							mode = cv2.RETR_EXTERNAL, \
							method = cv2.CHAIN_APPROX_NONE)
	cv2.drawContours( image = canvas, \
					contours = contours, \
					contourIdx = -1, \
					color = (255,255,255))
	for cnt in contours:
		hull = cv2.convexHull(cnt,returnPoints = False)
		defects = cv2.convexityDefects(cnt,hull)
		for i in range(defects.shape[0]):
			s,e,f,d = defects[i,0]
			start = tuple(cnt[s][0])
			end = tuple(cnt[e][0])
			far = tuple(cnt[f][0])
			cv2.line(canvas,start,end,[0,255,0],2)
			cv2.circle(canvas,far,5,[0,0,255],-1)
		####
	####
	"""
	cv2.namedWindow("cats")
	cv2.imshow("cats",canvas)
	cv2.imwrite(prefix+"KMEANS_orange_test.png",canvas)
	waitForKeyPress()
####

if __name__=="__main__":
	main()
####
