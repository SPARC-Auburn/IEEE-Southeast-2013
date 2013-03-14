from os import path
import cv2
import numpy as np

"""This program is meant as a tool to visualize the colorspaces at the moment
only the CRCB colorspace picture has been generated. More may be generated in the 
future
"""

def main():
	border = 10

	drawHVspace_draft2()
	drawCRCBspace_draft2()

	drawCRCBspace_draft1()
	drawHVspace_draft1()
	
####

def drawHVspace_draft2():
	## border | 256 | border
	## [0,1,...,border-1, | border+0, border+1, ..., border+255 | border+256,...256+(2*border)-1]
	border = 10
	hv_space_canvas = np.zeros([2*border+256,2*border+256,3],np.uint8)
	hv_space = hv_space_canvas[border:(border+256-1),border:(border+256-1),:]
	hv_space[:,:,:] = 96
	
	##HSV
	##			 [Hue,Sat,Val]

	black_hsv = Threshold( name = "black", \
		color = (0,0,0), \
		lowerb = ( 16, 29,130), \
		upperb = (108,194,152) )
	red1_hsv = Threshold( name = "red", \
		color = (0,0,255), \
		lowerb = ( 32,147,116), \
		upperb = ( 61,224,155) )
	red2_hsv = Threshold( name = "red", \
		color = (0,0,255), \
		lowerb = (231,129, 89), \
		upperb = (159,238,166) )
	orange_hsv = Threshold( name = "orange", \
		color = (0,100,230), \
		lowerb = (  6,154, 47), \
		upperb = (218,222,101) )
	yellow_hsv = Threshold( name = "yellow", \
		color = (0,255,255), \
		lowerb = (  0,108,  0), \
		upperb = (255,143,101) )
	green_hsv = Threshold( name = "green", \
		color = (0,255,0), \
		lowerb = (  0,108, 82), \
		upperb = ( 60,123,130) )
	blue_hsv = Threshold( name = "blue", \
		color = (255,0,0), \
		lowerb = (  9,  0,154), \
		upperb = ( 78,255,254) )
	brown_hsv = Threshold( name = "brown", \
		color = (0,77,108), \
		lowerb = (  6,133, 18), \
		upperb = ( 27,205,236) )

	##X axis
	cv2.rectangle(hv_space,(0,255),(255,254),(255,255,255),-1,cv2.CV_AA)
	##Y axis
	cv2.rectangle(hv_space,(0,0),(1,255),(255,255,255),-1,cv2.CV_AA)

	color_list = [red1_hsv,red2_hsv,orange_hsv,yellow_hsv,green_hsv,blue_hsv,brown_hsv,black_hsv]
	##Hue is the x coordinate
	##Value is the y coordinate
	for t in color_list:
		tpt1 = (t.lowerb[0],255-t.lowerb[2])
		tpt2 = (t.upperb[0],255-t.upperb[2])
		cv2.rectangle(hv_space,tpt1,tpt2,t.color,-1,cv2.CV_AA)
	####
	(workingdir,exec_ext) = path.split(path.realpath(__file__))

	cv2.namedWindow("^vValue,<>Hue: Draft #2")
	cv2.imshow("^vValue,<>Hue: Draft #2",hv_space_canvas)
	cv2.imwrite(workingdir+"/^vValue,<>Hue ColorSpace Visualization Draft_2.png",hv_space_canvas)
	return hv_space_canvas	
####

def drawCRCBspace_draft2():
	## border | 256 | border
	## [0,1,...,border-1, | border+0, border+1, ..., border+255 | border+256,...256+(2*border)-1]
	border = 10
	crcb_space_canvas = np.zeros([2*border+256,2*border+256,3],np.uint8)
	crcb_space = crcb_space_canvas[border:(border+256-1),border:(border+256-1),:]
	
	crcb_space[:,:,:] = 96
	##CB is x coordinate
	##CR is y coordinate

	##Draw YCR_CB Colors
	##YCR_CB threshold values 
	black_ycrcb = Threshold( name = "black", \
		color = (0,0,0), \
		lowerb = ( 15, 94,129), \
		upperb = ( 86,130,140) )
	red_ycrcb = Threshold( name = "red", \
		color = (0,0,255), \
		lowerb = (  6,139,118), \
		upperb = ( 72,195,126) )
	orange_ycrcb = Threshold( name = "orange", \
		color = (0,100,230), \
		lowerb = ( 41,154, 44), \
		upperb = (176,202,102) )
	yellow_ycrcb = Threshold( name = "yellow", \
		color = (0,255,255), \
		lowerb = ( 37,122, 14), \
		upperb = (243,141,108) )
	green_ycrcb = Threshold( name = "green", \
		color = (0,255,0), \
		lowerb = (  3, 98,109), \
		upperb = ( 37,124,130) )
	blue_ycrcb = Threshold( name = "blue", \
		color = (255,0,0), \
		lowerb = (  2, 74,154), \
		upperb = ( 43,143,129) )
	brown_ycrcb = Threshold( name = "brown", \
		color = (0,77,108), \
		lowerb = ( 14,133,127), \
		upperb = ( 43,143,129) )

	##X axis
	cv2.rectangle(crcb_space,(0,255),(255,254),(255,255,255),-1,cv2.CV_AA)
	##Y axis
	cv2.rectangle(crcb_space,(0,0),(1,255),(255,255,255),-1,cv2.CV_AA)

	color_list = [red_ycrcb,orange_ycrcb,yellow_ycrcb,green_ycrcb,blue_ycrcb,brown_ycrcb,black_ycrcb]
	##CB is the x coordinate
	##CR is the y coordinate
	for t in color_list:
		tpt1 = (t.lowerb[2],255-t.lowerb[1])
		tpt2 = (t.upperb[2],255-t.upperb[1])
		cv2.rectangle(crcb_space,tpt1,tpt2,t.color,-1,cv2.CV_AA)
	####
	(workingdir,exec_ext) = path.split(path.realpath(__file__))

	cv2.namedWindow("^vCR,<>CB: Draft #2")
	cv2.imshow("^vCR,<>CB: Draft #2",crcb_space_canvas)
	cv2.imwrite(workingdir+"/^vCR,<>CB ColorSpace Visualization Draft_2.png",crcb_space_canvas)
	return crcb_space_canvas
####

#####################################
#####################################

def drawHVspace_draft1():
	## border | 256 | border
	## [0,1,...,border-1, | border+0, border+1, ..., border+255 | border+256,...256+(2*border)-1]
	border = 10
	hv_space_canvas = np.zeros([2*border+256,2*border+256,3],np.uint8)
	hv_space = hv_space_canvas[border:(border+256-1),border:(border+256-1),:]
	hv_space[:,:,:] = 96
	
	##HSV
	##			 [Hue,Sat,Val]
	black_low	=[140,  0, 41] 
	black_high	=[125, 39, 61]
	blackc = (0,0,0)
	black = [black_low,black_high,blackc]

	red_low1	=[  0,165, 61]	   
	red_high1	=[  6,212,126]
	redc = (0,0,255)
	red1 = [red_low1,red_high1,redc]

	red_low2	=[169,165, 61]
	red_high2	=[179,212,126]
	redc = (0,0,255)
	red2 = [red_low2,red_high2,redc]

	orange_low	=[  4,186,108]
	orange_high	=[ 13,255,255]
	orangec = (0,100,230)
	orange = [orange_low,orange_high,orangec]
			  
	yellow_low	=[ 21,148, 97]
	yellow_high	=[ 32,255,255]
	yellowc = (0,255,255)
	yellow = [yellow_low,yellow_high,yellowc]
					  
	green_low	=[ 54, 74, 44]
	green_high	=[ 78,140, 77]
	greenc = (0,255,0)
	green = [green_low,green_high,greenc]
						  
	blue_low	=[108,168, 41]
	blue_high	=[121,255,202]
	bluec = (255,0,0)
	blue = [blue_low,blue_high,bluec]
	  
	brown_low	=[  2, 74, 51]
	brown_high	=[ 15,204, 84]  
	brownc = (0,77,108)
	brown = [brown_low,brown_high,brownc]


	##X axis
	cv2.rectangle(hv_space,(0,255),(255,254),(255,255,255),-1,cv2.CV_AA)
	##Y axis
	cv2.rectangle(hv_space,(0,0),(1,255),(255,255,255),-1,cv2.CV_AA)

	color_list = [red1,red2,orange,yellow,green,blue,brown,black]
	##Hue is the x coordinate
	##Value is the y coordinate
	for ((h1,s1,v1) ,(h2,s2,v2) ,color) in color_list:
		tpt1 = (h1,255-v1)
		tpt2 = (h2,255-v2)
		cv2.rectangle(hv_space,tpt1,tpt2,color,-1,cv2.CV_AA)
	####
	(workingdir,exec_ext) = path.split(path.realpath(__file__))

	cv2.namedWindow("^vValue,<>Hue: Draft #1")
	cv2.imshow("^vValue,<>Hue: Draft #1",hv_space_canvas)
	cv2.imwrite(workingdir+"/^vValue,<>Hue ColorSpace Visualization Draft_1.png",hv_space_canvas)
	return hv_space_canvas	
####

def drawCRCBspace_draft1():
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
	cv2.rectangle(crcb_space,(0,255),(255,254),(255,255,255),-1,cv2.CV_AA)
	##Y axis
	cv2.rectangle(crcb_space,(0,0),(1,255),(255,255,255),-1,cv2.CV_AA)

	color_list = [red,orange,yellow,green,blue,brown,black]
	for (pt1,pt2,color) in color_list:
		tpt1 = (pt1[0],255-pt1[1])
		tpt2 = (pt2[0],255-pt2[1])
		cv2.rectangle(crcb_space,tpt1,tpt2,color,-1,cv2.CV_AA)
	####
	(workingdir,exec_ext) = path.split(path.realpath(__file__))

	cv2.namedWindow("^vCR,<>CB: Draft #1")
	cv2.imshow("^vCR,<>CB: Draft #1",crcb_space_canvas)
	cv2.imwrite(workingdir+"/^vCR,<>CB ColorSpace Visualization Draft_1.png",crcb_space_canvas)
	return crcb_space_canvas
####


class Threshold():
	"""
	This class is just a glorified struct...
	name    :   string
	color   :   (3 tuple)
	lowerb  :   (3 tuple)
	upperb  :   (3 tuple)
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
####





if __name__=="__main__":
	main()
####
