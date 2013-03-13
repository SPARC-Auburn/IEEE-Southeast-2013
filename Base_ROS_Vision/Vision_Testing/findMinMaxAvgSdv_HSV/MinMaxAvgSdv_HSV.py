## Author: Patrick Berry
## Purpose: Find the Mininum, Maximum, Average, Standard Deviation of the HueSatVal channels given a list of images in a file
## Last Updated 2013-02-21
## 

## Cats
"""Okay.... so this program is outdated by the MinMaxAvgSdv_HSV_cv2.py mainly because
THIS ONE USES AN OLD VERSION OF OPENCV

I didn't know the cv was outdate at the time I wrote this, but when I realized 
I raged so hard that I wrote the another script that did the same thing, but used cv2.
Anywho, this thing takes in a filelist of files
and finds the MinMaxAvgSdv of the HSV of each file found.

Yeah, stop reading this and head over to MinMaxAvgSdv_HSV_2.py
"""

from cv import SetImageCOI,MinMaxLoc,LoadImage,AvgSdv,CV_BGR2HSV,CvtColor
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
		img = LoadImage(fileName)

		## Converts the image from BlueGreenRed to HueSaturationValue
		CvtColor(img,img,CV_BGR2HSV)

		## Lists that hold values for each channel
		min = []
		max = []
		avg = []
		sdv = []

		#Loop through all the channels. Ignores ch4/alpha channel
		for i in xrange(3):
			## Sets ChannelOfInterest 
			## COI starts at 1, (0 means no COI)
			SetImageCOI(img,i+1)

			(tempMin,tempMax,minLoc,maxLoc) = MinMaxLoc(img)
			min.append(tempMin)
			max.append(tempMax)
			(tempAvg,tempSdv) = AvgSdv(img)
			## AvgSdv returns a list with two cvScalars [avg,sdv]
			## but since the COI is set only the first one contains any
			## useful information
			avg.append(tempAvg[0])
			sdv.append(tempSdv[0])
		####

		print "\n",fileName
		print "\tMin:\t",min
		print "\tMax:\t",max
		print "\tAvg:\t",avg
		print "\tSdv:\t",sdv
	####
	print "\n\n"
####


if __name__=="__main__":
	main()
####
