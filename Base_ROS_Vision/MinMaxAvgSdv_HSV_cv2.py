## Author: Patrick Berry
## Purpose: Find the Mininum, Maximum, Average, Standard Deviation of the HueSatVal channels given a list of images in a file
## Last Updated 2013-02-21
## 

## Cats

from cv2 import imread,cvtColor,COLOR_BGR2HSV,split
import numpy as np
from sys import argv

def main():
	## CHecks to make sure there is the correct number of command line arguments
	if( argv.__len__() != 2):
		print "\nError\nUsage: MinMaxAvgSdv_HSV.py fileList.txt\n"
		return -1
	####

	## Opens the filelist and reads in all the flieNames
	fileHandle = open(argv[1],'r')
	fileList = [line.strip() for line in fileHandle]
	fileHandle.close()
	
	print "\n\nMin/Max/Avg/Sdv for HSV values for images found in:\n",argv[1]
	for fileName in fileList:

		## ignores any blank lines
		if( fileName == '' ):
			continue
		####

		## Opens the image
		img = imread(fileName)
		
		if( img == None ):
			print "\nCould not open file:\n",fileName
			continue
		####

		## Converts the image from BGR to HSV
		img = cvtColor(img,COLOR_BGR2HSV)

		## Splits the image into three separate channels		
		(img_h,img_s,img_v) = split(img)

		## Lists that hold values for each channel
		min = [ img_h.min(), img_s.min(), img_v.min() ]
		max = [ img_h.max(), img_s.max(), img_v.max() ]
		avg = [ img_h.mean(), img_s.mean(), img_v.mean() ]
		std = [ img_h.min(), img_s.min(), img_v.min() ]

		print "\n",fileName
		print "\tMin:\t",min
		print "\tMax:\t",max
		print "\tAvg:\t",avg
		print "\tSdv:\t",std
	####
	print "\n\n"
####


if __name__=="__main__":
	main()
####
