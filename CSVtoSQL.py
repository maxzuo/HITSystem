import sqlite3
import sys
import argparse
import os
from datetime import datetime

if int(sys.version_info[0]) >= 3:
	from functools import reduce


parser = argparse.ArgumentParser()
parser.add_argument("-c", "--csv", type=str, help="set the filepath to the csv file you would like to add to the server")
parser.add_argument("-db", "--database", type=str, help="set the filepath to the sqlite3 server you would like to have the csv added to")
parser.add_argument("-ct", "--coltypes", type=str, help="the type of each column")
parser.add_argument("-t", "--tablename", type=str, help="name of the table you want to create")

csv = None
database = None

def format(line, coltypes):
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
		else:
			raise(Exception(y + " type is either not currently supported or is not a datatype"))
	# print tuple(formatted)
	# sys.exit()
	return formatted

def create_table(tableName, cols, fail=False):
	table_command = "CREATE TABLE %s (%s);" % (tableName, cols)
	try:
		c.execute(table_command)
		print("%s table made" % tableName)
	except Exception as e:
		print(e)
		if not fail:
			print("Dropping the table, trying again")
			c.execute("DROP TABLE %s;" % tableName)
			create_table(tableName, cols, fail=True)
		else:
			print("Unable to create table")
			raise(e)



if __name__ == "__main__":
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
		coltypes = (args.coltypes).replace("\n", "").replace("\r", "").split(" ")
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

	#
	cols = reduce(lambda x, y: x + ", " + y, map(lambda a: a[0] + " " + a[1], zip(cols, coltypes)))

	create_table(tableName, cols)
	csvProcessed = map(lambda line: format(line, coltypes), csv)
	for line in csvProcessed:
		insert_command = "INSERT INTO %s VALUES (%s);" % (tableName, reduce(lambda x, y: x + ", " + y, ["?" for i in range(len(coltypes))]))
		c.execute(insert_command, line)

	print("Everything inserted!")
	database.commit()
	database.close()





























