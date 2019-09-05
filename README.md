# pyopenms to openms
project: port of python script to Cpp for pyopenms featureXML to SQL db conversion  

23.08.2019: 4 files updated, which in the end should compose the total of the python project
with compare.py being main script, export and import submodules 

26.08.2019: refactored code, export of subordinates table modularized partially 
should serve as template for features, dataprocessing tables

04.09.2019: import.py is able to read tables,
access of main feature setters almost for output.featureXML,
subordinate access and getKeys() as well as conditionals not implemented

05.08.2019: import.py stores about 80% of relevant information of featureXMLs
condititional looping and subordinate case matching required
