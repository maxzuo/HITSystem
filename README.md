# HITSystem
A collection of scripts used for VIP Concussion Connect to process HITS data.

## Using `CSVtoSQL.py`

`CSVtoSQL.py` is a Python script which should be run from the command line. `CSVtoSQL.py` is currently supported for both Python 2.x and Python 3.x. `CSVtoSQL.py` will create a table and insert each row as a data element into a specified **SQLite** database. `CSVtoSQL.py` works by taking a CSV file where the first row has your column names and the rest are your data entries. You must also provide a string of data types which correlate to your columns in your CSV file. To run this script, type in the command line:

    python CSVtoSQL.py -c "[csv file path]" -db "[SQLite database file path]" -ct "[data element types]" -t "[table name]"

Ex:

    python CSVtoSQL.py -c "calculations.csv" -db "hits.db" -ct "int float varchar(255) date time" -t "PRACTICES"

* CSV file path. Path to the CSV file you wish to add as a table to your database.
* SQLite databsae file path. File path to the SQLite database you wish to add to.
* Data element types. SQLite types which correlate to each column in the CSV file.
    * Supported types include: int, float, varchar, char. *Support for date and time are coming soon.*

### Tips & Debugging:
* Be sure that your file paths and strings are surrounded in quotation marks.
* Make sure you are currently in the same directory as `CSVtoSQL.py`
* If it still isn't working, try using the absolute path for everything, including `CSVtoSQL.py`, the csv file path, and the SQLite database file path.

### Get Started
1. Clone the repository
2. Move the `CSVtoSQL.py` to the directory containing your key file and raw file.
3. Go into your command line tool, change directories to the directory containing your files.
4. Run `CSVtoSQL.py` as shown above. 

## Using `convertHIT.py`

`convertHIT.py` is a Python script which can be run from the command line. This script will take a raw HITS file and convert it into a readable tab-separated-variable file (.tsv) which can then be opened by applications such as Microsoft Excel or Google Sheets. To run the script, type in the command line:

    python convertHIT.py "[raw file path]" "[key file path]" "[destination file path]"

Ex:

    python convertHIT.py "HITSRAW" "key.tsv" "converted.tsv"

* Raw file path. Path to the raw HITS file to convert.
* Key file path. Path to your "keys" .tsv file.
* Destination file path. An empty file path with the pattern `*.tsv`. convertHIT.py writes a .tsv file.

### Tips & Debugging:
* Be sure that your file paths are surrounded in quotation marks.
* Make sure you are currently in the same directory as `convertHIT.py`
* If it still isn't working, try using the absolute path for everything, including `convertHIT.py`, the raw file path, key file path, and destination file path.

### Keys file
Your "keys" .tsv file should have the following setup:

* The first column should be the title of data elements you want in your **processed** .tsv file.
* The second column should be the title of data elements in the **raw** file which correspond to those in the first column.

#### Note: `convertHIT.py` is currently only supported by Python 2.x. **HITSystem** will have full support for Python3 before January 1, 2020.

### Get Started
1. Clone the repository
2. Move the `convertHIT.py` to the directory containing your key file and raw file.
3. Go into your command line tool, change directories to the directory containing your files.
4. Run `convertHIT.py`

