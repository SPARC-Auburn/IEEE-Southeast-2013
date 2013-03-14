"""
Okay so this thing takes in a list of images as arguments
and spits out colorspace statistics for each image

--ColorSpace_Testing_<CurrentTime>/
---Image/ (for every image given)
----Stats.txt
----ColorSpace/ (for ever color-space specified)
-----Ch1NoBlur.png
-----Ch1PreBlur.png
-----Ch1PostBlur.png
----Ch1BothBlur.png
-----...(Ch2 and Ch3)
-----HistNoBlur.png
-----....etc

If you want to look at the statistics for a particular ColorSpace use
grab_COLORSPACE_data.py 
"""


import cv2
import numpy as np
from random import random
from sys import argv
from os import path,mkdir
from time import time
def main():

	if( argv.__len__() < 2 ):
		print "\nError\nUsage: *.py (filename)"
		return -1
	####
	(workingdir,exec_ext) = path.split(path.realpath(__file__))
	pathlist = argv[1:]

	curtime = int(time())

	##Create a base subfolder for the entire procedure
	base_prefix = workingdir + "/ColorSpace_Testing_"+str(curtime)
	mkdir(base_prefix)
	base_prefix = base_prefix + "/"
	ext    = ".png"
	iter   = 15

	conversion_dict = {"LUV":cv2.COLOR_BGR2LUV,"HSV":cv2.COLOR_BGR2HSV,"YUV":cv2.COLOR_BGR2YUV,"YCR_CB":cv2.COLOR_BGR2YCR_CB,"RGB":cv2.COLOR_BGR2RGB,"HLS":cv2.COLOR_BGR2HLS,"XYZ":cv2.COLOR_BGR2XYZ}

	##Loop over all provided files (images)
	for pathname in pathlist:
		(curdir,filename_ext) = path.split(pathname)
		(filename,ext) = path.splitext(filename_ext)
		
		original = cv2.imread(pathname)

		if( original == None ):
			print "\nError\nFile ",pathname," could not be found"
			continue
		####

		##Create a subfolder for every provided file
		file_prefix = base_prefix+filename
		mkdir(file_prefix)
		file_prefix = file_prefix + "/"

		output = []
		##Loop over all conversions specified
		for (name,conv) in conversion_dict.items():
			##Create a subfolder for every conversion
			prefix = file_prefix + name
			mkdir(prefix)
			prefix = prefix + "/"

			output.append("\n\n"+name)

			########
			##No Blur		
			img = cv2.cvtColor(original,conv)
			(ch1,ch2,ch3) = cv2.split(img)
			cv2.imwrite(prefix+"Ch1_NoBlur"+ext,ch1)
			cv2.imwrite(prefix+"Ch2_NoBlur"+ext,ch2)
			cv2.imwrite(prefix+"Ch3_NoBlur"+ext,ch3)

			##I have to write it to a file and then re-read it because opencv2 is idiotic
			hist = create3ChannelHistogram(cv2.merge([ch1,ch2,ch3]))
			cv2.imwrite(prefix+"Hist_NoBlur"+ext,hist)
			hist = cv2.imread(prefix+"Hist_NoBlur"+ext)
			cv2.putText(hist,"BGR:"+name,(15,30),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,255,255),thickness = 1, lineType = cv2.CV_AA)
			cv2.imwrite(prefix+"Hist_NoBlur"+ext,hist)

			output.append("\nNo Blur")
			output.append("\nCh1:")
			output.append(get_stats(ch1))
			output.append("\nCh2:")
			output.append(get_stats(ch2))
			output.append("\nCh3:")
			output.append(get_stats(ch3))
			########

			########
			##HSV Pre-Blur
			for i in xrange(iter):
				ch1 = cv2.medianBlur(ch1,3)
				ch2 = cv2.medianBlur(ch2,3)
				ch3 = cv2.medianBlur(ch3,3)
			####
			cv2.imwrite(prefix+"Ch1_PreBlur"+ext,ch1)
			cv2.imwrite(prefix+"Ch2_PreBlur"+ext,ch2)
			cv2.imwrite(prefix+"Ch3_PreBlur"+ext,ch3)

			##I have to write it to a file and then re-read it because opencv2 is idiotic
			hist = create3ChannelHistogram(cv2.merge([ch1,ch2,ch3]))
			cv2.imwrite(prefix+"Hist_PreBlur"+ext,hist)
			hist = cv2.imread(prefix+"Hist_PreBlur"+ext)
			cv2.putText(hist,"BGR:"+name,(15,30),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,255,255),thickness = 1, lineType = cv2.CV_AA)
			cv2.imwrite(prefix+"Hist_PreBlur"+ext,hist)

			output.append("\nPreBlur")
			output.append("\nCh1:")
			output.append(get_stats(ch1))
			output.append("\nCh2:")
			output.append(get_stats(ch2))
			output.append("\nCh3:")
			output.append(get_stats(ch3))
			########

			########
			##HSV Post-Blur
			img = cv2.cvtColor(original,conv)
			for i in xrange(iter):
				img = cv2.medianBlur(img,3)
			####
			(ch1,ch2,ch3) = cv2.split(img)
			cv2.imwrite(prefix+"Ch1_PostBlur"+ext,ch1)
			cv2.imwrite(prefix+"Ch2_PostBlur"+ext,ch2)
			cv2.imwrite(prefix+"Ch3_PostBlur"+ext,ch3)

			##I have to write it to a file and then re-read it because opencv2 is idiotic
			hist = create3ChannelHistogram(cv2.merge([ch1,ch2,ch3]))
			cv2.imwrite(prefix+"Hist_PostBlur"+ext,hist)
			hist = cv2.imread(prefix+"Hist_PostBlur"+ext)
			cv2.putText(hist,"BGR:"+name,(15,30),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,255,255),thickness = 1, lineType = cv2.CV_AA)
			cv2.imwrite(prefix+"Hist_PostBlur"+ext,hist)

			output.append("\nPostBlur")
			output.append("\nCh1:")
			output.append(get_stats(ch1))
			output.append("\nCh2:")
			output.append(get_stats(ch2))
			output.append("\nCh3:")
			output.append(get_stats(ch3))
			########

			########
			##HSV BothBlur
			for i in xrange(iter):
				ch1 = cv2.medianBlur(ch1,3)
				ch2 = cv2.medianBlur(ch2,3)
				ch3 = cv2.medianBlur(ch3,3)
			####
			cv2.imwrite(prefix+"Ch1_BothBlur"+ext,ch1)
			cv2.imwrite(prefix+"Ch2_BothBlur"+ext,ch2)
			cv2.imwrite(prefix+"Ch3_BothBlur"+ext,ch3)

			##I have to write it to a file and then re-read it because opencv2 is idiotic
			hist = create3ChannelHistogram(cv2.merge([ch1,ch2,ch3]))
			cv2.imwrite(prefix+"Hist_BothBlur"+ext,hist)
			hist = cv2.imread(prefix+"Hist_BothBlur"+ext)
			cv2.putText(hist,"BGR:"+name,(15,30),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,255,255),thickness = 1, lineType = cv2.CV_AA)
			cv2.imwrite(prefix+"Hist_BothBlur"+ext,hist)

			output.append("\nBothBlur")
			output.append("\nCh1:")
			output.append(get_stats(ch1))
			output.append("\nCh2:")
			output.append(get_stats(ch2))
			output.append("\nCh3:")
			output.append(get_stats(ch3))
			########
		####
		output_file = open(file_prefix+"MinMaxAvgSdv.txt",'w')
		output_file.write(''.join(output))
		output_file.close()
	####

	return 0
####

def create3ChannelHistogram(img):
	h = np.zeros((300,256,3))

	bins = np.arange(256).reshape(256,1)
	color = [ (255,0,0),(0,255,0),(0,0,255) ]

	##Blue  == Ch1
	##Green == Ch2
	##Red   == Ch3
	for ch, col in enumerate(color):
		hist_item = cv2.calcHist([img],[ch],None,[256],[0,256])
		cv2.normalize(hist_item,hist_item,0,255,cv2.NORM_MINMAX)
		hist=np.int32(np.around(hist_item))
		pts = np.column_stack((bins,hist))
		cv2.polylines(h,[pts],False,col)
	####
	h=np.flipud(h)
	return h
####

def get_stats(img):
	min = str(img.min())
	max = str(img.max())
	avg = str(img.mean())
	sdv = str(img.std())
	return '\t'.join([min,max,avg,sdv])
####

if __name__=="__main__":
	main()
####
