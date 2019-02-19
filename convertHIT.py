import sys
import os
from datetime import datetime

#Converts HIT src to tsv using key and saving it to dest
def convert(src, key, dest, verbose=False):
	now = datetime.now()
	if (not os.path.isfile(src)):
		raise Exception("The provided source filepath is not a file: %s" % src)
	if (not os.path.isfile(key)):
		raise Exception("The provided key filepath is not a file: %s" % src)
	
	#Retrieve and process raw data. Hardcoding to ignore the first 5 lines
	#and the 7th line (not important)
	raw = process(readLines(src))

	#Printing metadata deleted when processing the file
	os.system("clear")
	print "Raw File:\t\t\t\t%s\n\nMetadata:\n" %src, reduce(lambda x,y: "\n".join([x,y]),
		map(lambda x: "\r\t\t\t\t\t".join(x), raw[:5]))
	matrix = raw[5:]
	matrix.pop(1)

	#calculating columns and rows so the resulting matrix will be rectangular
	cols = max([len(line) for line in matrix])
	rows = len(matrix)

	#recreating tsv as a matrix. Not completely necessary
	for line in matrix:
		while len(line) < cols:
			line.append("")

	#Retrieve keys and store in a dictionary
	# print matrix[0]

	keys = process(readLines(key))
	keyDict = {}
	for key in keys:
		keyDict[key[1]] = key[0]
	
	#Array tagged used to remember indices of desired elements
	tagged = []

	for i in xrange(cols):
		try:
			matrix[0][i] = keyDict[matrix[0][i]]
			tagged.append(i)
		except:
			pass

	#Write new file at destinated file path
	with open(dest, "w") as destFile:
		for i in xrange(rows):
			line = []
			for j in xrange(cols):
				if j == 0 or j in tagged:
					line.append(matrix[i][j])
			destFile.write("\t".join(line) + "\n")
	
	print "\n\nProcessed file saved at:\t\t%s\n" % dest
	if verbose:
		print "Conversion took\t\t\t\t%s\n" % str(datetime.now() - now)

	
#Wrapper function to open, read, and then close a file
#Returns an array of lines
def readLines(src):
	src = open(src, "r")
	lines = src.readlines()
	src.close()
	return lines

#Wrapper function to process and clean tsv files
#Returns tsv back
def process(tsv):
	tsv = [line.replace("\r\n", "").replace("\n", "") for line in tsv]
	tsv = map(lambda line: line.split("\t"), tsv)
	for line in tsv:
		try:
			line.remove("")
		except:
			pass
	return tsv



if __name__ == "__main__":
	if len(sys.argv) != 4:
		print "You must provide a source filepath, key filepath, and a destination filepath"
		print "python convertHIT.py [source] [key] [destination]"
		sys.exit()
	convert(sys.argv[1], sys.argv[2], sys.argv[3])