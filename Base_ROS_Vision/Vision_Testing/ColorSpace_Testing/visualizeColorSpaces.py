from os import path
import cv2
import numpy as np

def main():
	border = 10
	hsv_space = np.zeros([2*border+256,2*border+256,3],np.uint8)

	drawCRCBspace()
####

def drawCRCBspace():
	## border | 256 | border
	## [0,1,...,border-1, | border+0, border+1, ..., border+255 | border+256,...256+(2*border)-1]
	border = 10
	crcb_space_canvas = np.zeros([2*border+256,2*border+256,3],np.uint8)
	crcb_space = crcb_space_canvas[border:(border+256-1),border:(border+256-1),:]
	
	crcb_space[:,:,:] = 96
	##CB is x coordinate
	##CR is y coordinate

	##Draw YCR_CB Colors
	##YCR_CB threshold values @ 1363153646.792677
	red1 = (107,148)
	red2 = (126,177)
	redc = (0,0,255)
	red = [red1,red2,redc]

	orange1 = (42,165)
	orange2 = (106,200)
	orangec = (0,100,230)
	orange = [orange1,orange2,orangec]

	yellow1 = (35,137)
	yellow2 = (90,150)
	yellowc = (0,255,255)
	yellow = [yellow1,yellow2,yellowc]

	green1 = (119,110)
	green2 = (128,123)
	greenc = (0,255,0)
	green = [green1,green2,greenc]

	blue1 = (140,85)
	blue2 = (198,126)
	bluec = (255,0,0)
	blue = [blue1,blue2,bluec]

	brown1 = (114,138)
	brown2 = (125,148)
	brownc = (0,77,108)
	brown = [brown1,brown2,brownc]

	black1 = (128,127)
	black2 = (133,128)
	blackc = (0,0,0)
	black = [black1,black2,blackc]

	##X axis
	cv2.rectangle(crcb_space,(0,128),(255,128),(255,255,255),-1,cv2.CV_AA)
	##Y axis
	cv2.rectangle(crcb_space,(128,0),(128,255),(255,255,255),-1,cv2.CV_AA)

	color_list = [red,orange,yellow,green,blue,brown,black]
	for (pt1,pt2,color) in color_list:
		tpt1 = (pt1[0],255-pt1[1])
		tpt2 = (pt2[0],255-pt2[1])
		print color
		cv2.rectangle(crcb_space,tpt1,tpt2,color,-1,cv2.CV_AA)
	####
	(workingdir,exec_ext) = path.split(path.realpath(__file__))

	cv2.namedWindow("^vCR,<>CB")
	cv2.imshow("^vCR,<>CB",crcb_space_canvas)
	cv2.imwrite(workingdir+"/^vCR,<>CB ColorSpace Visualization.png",crcb_space_canvas)
	while( 1 ):
		if( cv2.waitKey( 15 ) == 27 ):
			return 0
		####
	####
####


if __name__=="__main__":
	main()
####
