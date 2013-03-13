
import cv2
import numpy as np
import time
from sys import argv

class MedianTest():
	"""
	This class tests many iterations and time it takes the MedianBlur filter to converge for different test images provided in the command line as well as the kernel_list and eps_list.
	"""
	def __init__(self):
		pass
	####

	def run(self):
		########
		##Check the arguments and grab the image
		if( argv.__len__()< 2 ):
			raise Exception("\nError\nUsage: *.py [fileName[,...]])")
		####
		filename_list = argv[1:]
		filename_len  = filename_list.__len__()
		outputFile = open("medianTest_output_"+str(time.time())+".txt","w")

		self.kernel_list = [3,5,7,9]
		self.eps_list = [3,5,10,15]

		kern_len = self.kernel_list.__len__()
		eps_len  = self.eps_list.__len__()

		self.data = np.zeros([filename_len,kern_len*eps_len,2])

		print filename_len," files found in command"
		i = 0
		for file_ind in xrange(filename_len): 

			self.original = cv2.imread(filename_list[file_ind])
	
			if( self.original == None ):
				raise Exception("\nError\ncould not open <"+fileName+">")
			####
			print i," ",filename_list[file_ind]
			(output,data) = self.medianTest(watch = False)	
			outputFile.write("\n"+filename_list[file_ind])
			outputFile.write(output)
			outputFile.write("\n")
			self.data[file_ind] = data.copy()
			i = i+1
		####

		outputFile.write("\nAverages across all images")
		output = []

		average = self.data.mean(0)
		for kern_ind in xrange(kern_len):
			for eps_ind in xrange(eps_len):
				output.append("\n"+str(self.kernel_list[kern_ind])+"\t"+str(self.eps_list[eps_ind])+"\t"+str(average[kern_ind*eps_len+eps_ind,0])+"\t"+str(average[kern_ind*eps_len+eps_ind,1]))
			####
		####
		outputFile.write(''.join(output))
	####

	def waitForKeyPress(self):
		while(1):
			keyPressed = cv2.waitKey(5)

			if( keyPressed != -1 ):
				return keyPressed
			####
		####
	####

	def medianTest(self,watch = False):
		if( watch == True):
			cv2.namedWindow("difference")
		####
		output = []

		kern_len = self.kernel_list.__len__()
		eps_len  = self.eps_list.__len__()

		data = np.zeros([kern_len*eps_len,2])

		for kern_ind in xrange(kern_len):
			for eps_ind in xrange(eps_len):
				output1 = self.original.copy()
				i = 0
				start_time  = time.time()
				while( 1 ):
					output2 = output1.copy()
					output1 = cv2.medianBlur(output1,self.kernel_list[kern_ind])
					difference = cv2.absdiff(output1,output2)
					i = i+1

					max = difference.max()
					if( max <= self.eps_list[eps_ind] or i >=500 ):
						elapsed_time = time.time()-start_time
						output.append("\n"+str(self.kernel_list[kern_ind])+"\t"+str(self.eps_list[eps_ind])+"\t"+str(i)+"\t"+str(elapsed_time))
						data[kern_ind*eps_len+eps_ind,0] = i
						data[kern_ind*eps_len+eps_ind,1] = elapsed_time
						break
					####
				####
			####
		####	
		return (''.join(output),data)	
	####
####

if __name__=="__main__":
	print "\n\nStart\n"
	test = MedianTest()
	test.run()
	print "\nFinish\n\n"
####



