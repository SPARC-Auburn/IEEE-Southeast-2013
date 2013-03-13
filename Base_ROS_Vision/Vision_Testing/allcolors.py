import cv

"""Produces an image with all possible colors
creates one 256x256 pattern with all Red and Green combinations
then it makes a 16x16 grid and adds 1 to the Blue value, so that
all possible 24bit colors are produced
"""

def main():
	##cv.NamedWindow('Input',0)
	maxCols = 16
	maxRows = 16
	img = cv.CreateMat(256*maxRows,256*maxCols,cv.CV_8UC3)

	for hue in xrange(256):
		for sat in xrange(256):
			for val in xrange(256):
				col = sat + (hue%maxCols)*255;
				row = val + ((hue/maxRows)%maxRows)*255;
				img[row,col] = (hue,sat,val)
			####
		####
	####
	
	cv.CvtColor(img,img,cv.CV_HSV2BGR)
	cv.SaveImage('cats.png',img)
	##cv.ShowImage('Input',img)
	##while(1):       
	##	if cv.WaitKey(10)==27:
	##		return 0;
	##		break
		####    
    ####
####


if __name__=="__main__":
	main()
####	

