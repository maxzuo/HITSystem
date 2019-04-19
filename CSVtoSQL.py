import sqlite3
import sys
import argparse
import os
from datetime import datetime
import re

if int(sys.version_info[0]) >= 3:
	from functools import reduce
	xrange = range
else:
	from six.moves import input


# NOTE: THE CURRENT IMPLEMENTATION OF THIS SCRIPT WILL OVERWRITE ANY TABLE WITH THE SAME NAME IN THE DATABASE
# 
# MEANING IT WILL DROP THE TABLE WITH THE SAME NAME BEFORE INSERTING!!!!!!!!!!!

parser = argparse.ArgumentParser()
parser.add_argument("-c", "--csv", type=str, help="set the filepath to the csv file you would like to add to the server")
parser.add_argument("-db", "--database", type=str, help="set the filepath to the sqlite3 server you would like to have the csv added to")
parser.add_argument("-ct", "--coltypes", type=str, help="the type of each column")
parser.add_argument("-t", "--tablename", type=str, help="name of the table you want to create")

csv = None
database = None

def format(line, coltypes):
	format.visited += 1
	format.visitedb += 1
	formatted = []
	for (x, y) in zip(line, coltypes):
		if x == "" or x.upper() == "N/A":
			formatted.append(None)
			continue

		if 'float' in y.lower():
			formatted.append(float(x))
		elif 'int' in y.lower():
			formatted.append(int(x))
		elif 'char' in y.lower():
			formatted.append(x)
		elif 'date' in y.lower():
			y = y.replace("date", '')
			r = re.compile('(\\(.*\\))', re.IGNORECASE|re.DOTALL).search(y)
			if r is None or len(r.groups()) > 1:
				raise(Exception("When using date, you provide a valid input for the formatting with the parentheses:\n%s" % y))
			accepted = False
			for i in xrange(len(x), 1, -1):
				try:
					# print(x[0:i])
					formatted.append(datetime.strptime(x[0:i], y[1:-1]))
					accepted = True
					if format.visited < 2 and i != len(x):
						print("Seems like your date element isn't an exact match to your formatter. To drastically speed up this process, please remove any leading/trailing characters")
						format.visited += 1
					break
				except Exception as e:
					continue
			if not accepted:
				raise(Exception("Could not format date. If there are any trailing/leading characters, try removing them. Otherwise, try editing your formatter"))
		elif 'time' in y.lower():
			y = y.replace("time", '')
			r = re.compile('(\\(.*\\))', re.IGNORECASE|re.DOTALL).search(y)
			if r is None or len(r.groups()) > 1:
				raise(Exception("When using time, you need provide a valid input for the formatting with the parentheses:\n%s" % y))
			accepted = False
			for i in xrange(len(x), 1, -1):
				try:
					# print(x[0:i])
					formatted.append(datetime.strptime(x[0:i], y[1:-1]))
					accepted = True
					if format.visitedb < 2 and i != len(x):
						print("Seems like the time element isn't an exact match to your formatter. To drastically speed up this process, please remove any leading/trailing characters")
						format.visitedb += 1
					break
				except Exception as e:
					continue
			if not accepted:
				raise(Exception("Could not format time. If there are any trailing/leading characters, try removing them. Otherwise, try editing your formatter"))
			

		else:
			raise(Exception(y + " type is either not currently supported or is not a datatype"))
	return formatted

def create_table(tableName, cols, fail=False):
	table_command = "CREATE TABLE %s (%s);" % (tableName, cols)
	try:
		c.execute(table_command)
		print("%s table made" % tableName)
	except Exception as e:
		print(e)
		overwrite = None
		while overwrite is None:
			x = input("Looks like the table already exists. You can choose to overwrite the table or insert to the current table. Overwrite? (y/n)\n").lower() 
			if "n" == x or "y" == x:
				overwrite = x
			else:
				print("Input unrecognized. Please type only 'y' or 'n' with nothing else.\n")
		if overwrite == 'y':
			if not fail:
				
				print("Dropping the table, trying again")
				c.execute("DROP TABLE %s;" % tableName)
				create_table(tableName, cols, fail=True)
			else:
				print("Unable to create table")
				raise(e)
		else:
			print("Will move on to try and insert the table.")



if __name__ == "__main__":
	format.visited = 0
	format.visitedb = 0
	print('')
	
	tableName = None
	coltypes = None


	#read in all the arguments from the argParser
	args = parser.parse_args()

	if args.csv != None:
		with open(args.csv, "r") as s:
			csv = list(map(lambda line: line.split(","), [line.replace("\r\n", "").replace("\n", "") for line in s.readlines()]))
	else:
		raise(Exception("Must provide a valid csv filepath"))
	if args.database != None and os.path.isfile(args.database):
		try:
			database = sqlite3.connect(args.database)
		except:
			raise(Exception("Must provide a valid sqlite3 database filepath"))
	else:
		raise(Exception("Must provide a valid sqlite3 database filepath"))
	if args.tablename != None:
		tableName = args.tablename
	else:
		raise(Exception("Must provide a table name. Use -t"))
	if args.coltypes != None:
		coltypes = list(((args.coltypes).replace("\n", "").replace("\r", "").split(" ")))
	else:
		raise(Exception("Must provide a list of column types which correlate to the csv. Use -ct"))


	# Cols represents the 'column names' in the SQLite database

	cols = csv.pop(0)


	for c in cols:
		for a in " ,./<>?;':\"\][{}|!@#$%^&*()_+=-":
			if a in c:
				raise(Exception("Illegal column header: Cannot have spaces, special characters: '%s'" % c))
	if len(cols) != len(coltypes):
		raise(Exception("Length of the columns found in csv not equivalent to the length of the column types provided.\n\nColumns: %d\n%s\n\nColumn types: %d\n%s" % (len(cols), cols, len(coltypes), coltypes)))

	c = database.cursor()

	cols = reduce(lambda x, y: x + ", " + (y.split(" ")[0] + " date" if " date" in y else y.split(" ")[0] + " time" if " time" in y else y), map(lambda a: a[0] + " " + a[1], zip(cols, coltypes)))

	csvProcessed = map(lambda line: format(line, coltypes), csv)
	create_table(tableName, cols)
	
	for line in csvProcessed:
		insert_command = "INSERT INTO %s VALUES (%s);" % (tableName, reduce(lambda x, y: x + ", " + y, ["?" for i in xrange(len(coltypes))]))
		c.execute(insert_command, line)

	print("Everything inserted!")
	database.commit()
	database.close()





























