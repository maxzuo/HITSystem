import sys
import os
from datetime import datetime


__version__ = "0.1.0"

#Converts HIT src to tsv using key and saving it to dest
def raw2tsv(src, key, dest=None, verbose=0):
	now = datetime.now() if verbose >= 2 else None

	if (not os.path.isfile(src)):
		raise Exception("The provided source filepath is not a file: %s" % src)
	if (key is not None and not os.path.isfile(key)):
		raise Exception("The provided key filepath is not a file: %s" % src)
	
	#Retrieve and process raw data. Hardcoding to ignore the first 5 lines
	#and the 7th line (not important)
	raw = __process(__readLines(src))

	#Printing metadata deleted when processing the file
	if verbose > 0:
		os.system("clear")
		print "Raw File:\t\t\t\t%s\n\nMetadata:\n" % src, reduce(lambda x,y: "\n".join([x,y]),
			map(lambda x: "\r\t\t\t\t\t".join(x), raw[:5])), "\n"
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

	if key is None:
		return __write(dest, __clean(matrix, None, rows, cols), time=now, verbose=verbose)

	keys = __process(__readLines(key))
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

	return __write(dest, __clean(matrix, tagged, rows, cols), time=now, verbose=verbose)

	
#Wrapper function to open, read, and then close a file
#Returns an array of lines
def __readLines(src):
	src = open(src, "r")
	lines = src.readlines()
	src.close()
	return lines

#Wrapper function to process and clean tsv files
#Returns tsv back
def __process(tsv):
	tsv = [line.replace("\r\n", "").replace("\n", "") for line in tsv]
	tsv = map(lambda line: line.split("\t"), tsv)
	for line in tsv:
		try:
			line.remove("")
		except:
			pass
	return tsv

#Helper method for writing the file
def __write(dest, cleaned, time=None, verbose=0):

	if dest is not None:
		with open(dest, "w") as destFile:
			for line in cleaned:
				destFile.write("\t".join(line) + "\n")
	
	if verbose > 0 and dest is not None:
		print "\nProcessed file saved at:\t\t%s\n" % dest
	if time is not None:
		print "Conversion took\t\t\t\t%s\n" % str(datetime.now() - time)
	return cleaned

def __clean(matrix, tagged, rows, cols):
	cleaned = []
	for i in xrange(rows):
		line = []
		for j in xrange(cols):
			if tagged is None or j == 0 or j in tagged:
				line.append(matrix[i][j])
		cleaned.append(line)
	return cleaned

# def tsv2hit

