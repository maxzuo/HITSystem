# HITSystem
A collection of scripts used for VIP Concussion Connect to process HITS data.

## Using `convertHIT.py`

`convertHIT.py` is a Python script which can be run from the command line. To do so, type:
    `python convertHIT.py "[raw file path]" "[key file path]" "[destination file path]"`

Be sure that your file paths are surrounded in quotation marks.

* Raw file path. Path to the raw HITS file to convert.
* Key file path. Path to your "keys" .tsv file.
* Destination file path. An empty file path with the pattern `*.tsv`. convertHIT.py writes a .tsv file.

### Keys file
Your "keys" .tsv file should have the following setup:

* The first column should be the title of data elements you want in your **processed** .tsv file.
* The second column should be the title of data elements in the **raw** file.
