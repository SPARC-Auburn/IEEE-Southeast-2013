from re import compile,IGNORECASE;
from sys import argv;
import os;

"""
This program is meant to be used after investigateColorSpaces.py has ran
Give this program a ColorSpace to search for and the Big Folder
investigateColorSpaces.py created. This script will grab the NoBlur statistics 
from each MinMaxAvgSdv.txt found in each image folder.
"""

def find_in_file(re_pattern,filename):
	fid = open(filename,'r')
	i=0
	matches = 0
	output = []
	
	##Sample Positive Identification
	"""
	YUV
	No Blur
	Ch1:23	56	44.6944444444	7.53443739861
	Ch2:136	141	139.055555556	1.43264410647
	Ch3:118	124	121.527777778	1.48110527631
	"""

	for line in fid:
		if( re_pattern.match(line) != None):
			matches = matches + 1
			continue
		####
		if( matches > 0 ):
			matches = matches + 1
		####
		if( matches > 2 ):
			output.append(line)
		####
		if( matches >=5 ):
			break
		####
		i = i+1
	####
	if(matches == 0):
		output.append("none")
		return ''
	####
	output.append("\n")
	fid.close()
	return ''.join(output)
####

def find_all_files_in_dir_tree(path):

	for path, dirs, files in os.walk(os.path.abspath(path)):
		for file in files:
			yield os.path.join(os.path.abspath(path),file)
		####
	####
####

def main():
	if( argv.__len__() != 3 ):
		print "\nError\nUsage search_all_subfolders_recursively.py 'pattern' 'pathname' \n"
		return 0
	####
	pattern = compile(argv[1])
	path = argv[2]
	(curdir,pathname) = os.path.split(path)

	##/Users/patrickberry/secon2013/Base_ROS_Vision/Vision_Testing/ColorSpace_Testing/Canny_Testing_1363074159
	outputFilename = curdir+"/"+argv[1]+"_data_for_"+pathname+".txt"
	output = []
	
	for pathname in find_all_files_in_dir_tree(path):
		(curdir,filename) = os.path.split(pathname)
		if( filename == "MinMaxAvgSdv.txt" ):
			(curdir,image_name) = os.path.split(curdir)	
			output.append("\n"+image_name+"\n")
			output.append(find_in_file(pattern,pathname))
		####
	outputFile = open(outputFilename,'w')
	outputFile.write(''.join(output))
	outputFile.close()
	print "done!"
####

if __name__ == "__main__":
	main()
####
		
