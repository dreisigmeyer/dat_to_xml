USPTO dat files for granted patents 1971-2001 are converted to XML documents.


## Python environment
This was designed using a standard Anaconda Python 3 installation:
https://www.anaconda.com/


## Running the code
The dat files can be automatically downloaded by running  
`./get_uspto_data.sh`  
The XML files are created using  
`nohup ./run_it.sh NUM_THREADS_TO_USE &`  
The output files are in the **xml_files** directory.
Each zipped folder contains the individual patent files named as _prdnnumb.xml_.
The directory **modified_xml_files** conatins the same files with the inventor information removed.


## Files
**dat_to_xml.py :**  
This gives the Python functions to convert the dat files to XML.  
```
iconvit_damnit(filename):
	Run iconv and sed on files that are being difficult.

	filename -- the file to run iconv on
```
```
sedit_damnit(filename):
	Some dat files have useless lines to make my life difficult.

	filename -- the file to run sed on
```
```
copy_dtds(dest_dir):
	copies the DTD files

	dest_dir -- the destination directory for the copied files
```
```
create_xml_file(dict_for_xml, wku, out_directory, mod_out_directory):
	Print the dictionary out to an xml file

	dict_for_xml -- the dictionary we're using to create the XML file
	wku -- the PRDN of the patent which becomes the name of the created XML file
	out_directory -- directory where the XML file is going to
	mod_out_directory -- directory where the XML file with inventors removed is going to
```
```
convert_to_xml(dat_files):
	Converts the USPTO dat files to XML files

	dat_files -- the files to convert including path information
```