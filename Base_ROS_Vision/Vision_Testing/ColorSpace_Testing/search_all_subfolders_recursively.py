
from re import compile,IGNORECASE;
from sys import argv;
import os;

"""
Okay so this thing searches all the files in every subfolder for a given string. 
Really this can be done by "grep pattern -r" but I happend to be working on a 
Windows at the time, so I wrote this baby to do it for me.
"""

def find_in_file(re_pattern,filename):
	fid = open(filename,'r')
	i=0
	matches = 0
	output = []
	output.extend(["\n",filename,"\n"])
	for line in fid:
		if( re_pattern.search(line) != None):
			output.extend([str(i),":",line])
			matches = matches + 1
		########
		i = i+1
	########
	if(matches == 0):
		output.append("none")
		return ''
	########
	output.append("\n")
	fid.close()
	return ''.join(output)
########

def find_all_files_in_dir_tree(path):

	for path, dirs, files in os.walk(os.path.abspath(path)):
		for file in files:
			yield os.path.join(os.path.abspath(path),file)
		########
	########
########

def main():
	if( argv.__len__() < 3 ):
		print "\nError\nUsage search_all_subfolders_recursively.py 'pattern' 'pathname' (ignore_case) \n"
		return 0
	########
	
	path = argv[2]
	pattern = argv[1]
	if( argv.__len__() >= 4 ):
		if( "ignore_case" == argv[3] ):
			re_pattern = compile(pattern, IGNORECASE)
		else:
			re_pattern = compile(pattern)
		########
	########
			

	outputFilename = "search_results_for_"+pattern+".txt"
	outputFile = open(outputFilename,'w')
	print "\n\nWriting to...\n",outputFilename
	outputFile.write("Search results for "+pattern+" in "+path+"\n")
	try:		
		for filename in find_all_files_in_dir_tree(path):
			outputFile.write(find_in_file(re_pattern,filename))
		########
	except:
		outputFile.close()
		raise
	########
	outputFile.close()
	print "done!"
########

if __name__ == "__main__":
	main()
########
		
