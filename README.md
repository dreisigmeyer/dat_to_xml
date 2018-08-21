USPTO dat files for granted patents 1971-2001 are converted to XML documents.

## Python environment
This was designed using a standard Anaconda Python 3 installation:
https://www.anaconda.com/

## Running the code
The dat files can be automatically downloaded by running  
`./get_uspto_data.sh`  
The XML files are created using  
`nohup ./run_it.sh &`  
The output files are in the **xml_files** directory.
Each zipped folder contains the individual patent files named as _prdnnumb.xml_.
The directory **modified_xml_files** conatins the same files with the inventor information removed.