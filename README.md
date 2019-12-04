## Table of Contents

* [Bachelor Project](#Bachelor-Project)
* [Breakdown](#Breakdown)
* [Timeline](#Timeline)

## Bachelor Project

This project was used as a tentative draft version for a SQLite database extension 
class, written for the [OpenMS framework](https://www.openms.de/), in Python using
its interface [pyOpenMS](https://pyopenms.readthedocs.io/en/latest/index.html).

## Breakdown
**pyopenms to openms

project parts
1. generate export script of FeatureMap objects in XML data format
2. generate import script to read SQLite database
3. porting of python scripts to Cpp for featureXML to SQL db conversion and back again

## Timeline in chronologically reversed order

23.08.2019: 4 files updated, which in the end should compose the total of the python project
with compare.py being main script, export, import and minor submodules 

26.08.2019: refactored code, export of subordinates table modularized partially 
should serve as template for features, dataprocessing tables

04.09.2019: import.py is able to read tables,
access of main feature setters almost for output.featureXML,
subordinate access and getKeys() as well as conditionals not implemented

05.09.2019: import.py stores about 80% of relevant information of featureXMLs
condititional looping and subordinate case matching required



