#exportDataProcTable
#read and store features from FeatureMap in csv format

#libs
import csv
import itertools
import os
import sqlite3
import enum

# libs for feature class
#from urllib.request import urlretrieve
from urllib import urlretrieve  # use this code for Python 2.x
from pyopenms import *

## variable definition
##input section
##output section
#sep = '\t'   #separator for file output
#write routine for file selection either local or via url
#gh = "https://raw.githubusercontent.com/OpenMS/OpenMS/develop"
#urlretrieve (gh + "/src/tests/topp/FeatureFinderCentroided_1_output.featureXML", "output.featureXML")
## input routine
## see https://stackoverflow.com/questions/11968976/list-files-only-in-the-current-directory
currentDirectory = os.getcwd()
#print(currentDirectory)
indexedFiles = []

## preselect outputXML file
files = [f for f in os.listdir('.') if os.path.isfile(f)]
files = filter(lambda file: file.endswith('.featureXML'), files)
counter = 1
for f in files:
  indexedFiles.append(f)
  print(str(counter) +' ' + f)
  counter += 1

## return selected file to output
## changed for testing purposes
#valueOfFileIndex = input("Enter featureXML index: ") - 1
#print('File selection: ' + indexedFiles[valueOfFileIndex] + '\n')

## read FeatureMap
features = FeatureMap()
filehandle = FeatureXMLFile()

#fh.load("output.featureXML", features)

## changed for testing purposes
#filehandle.load(indexedFiles[valueOfFileIndex], features)
filehandle.load(indexedFiles[1], features)
print(indexedFiles[1])
#1st sanity check
print("Found " + str(features.size()) + " features")
#store in separate file as backup?
#FeatureXMLFile().store("test.out.featureXML", features)
##preliminary output to console
### user params


#print(type(features))
dpr = features.getDataProcessing()
#print(dpro[0].getSoftware().getName())
print("\n")

procActionSwitch = {
  0: "DATA_PROCESSING",
  1: "CHARGE_DECONVOLUTION",
  2: "DEISOTOPING",
  3: "SMOOTHING",
  4: "CHARGE_CALCULATION",
  5: "PRECURSOR_RECALCULATION",
  6: "BASELINE_REDUCTION",
  7: "PEAK_PICKING",
  8: "ALIGNMENT",
  9: "CALIBRATION", 
  10:"NORMALIZATION",
  11:"FILTERING",
  12:"QUANTITATION",
  13:"FEATURE_GROUPING",
  14:"IDENTIFICATION_MAPPING",
  15:"FORMAT_CONVERSION",
  16:"CONVERSION_MZDATA",
  17:"CONVERSION_MZML",
  18:"CONVERSION_MZXML",
  19:"CONVERSION_DTA",
  20:"SIZE_OF_PROCESSINGACTION"
}

#print(dpr[0].getSoftware().getName())

dpElems = []
dpElems.append(str(features.getUniqueId()))

for p in dpr:
  #print(features.getUniqueId())
  #print(p.__class__.__name__)
  #print(type(p))  
  #print(p.getCompletionTime().getDate())
  #print(p.getCompletionTime().getTime())
  #print (p.getSoftware().getName())
  #  print(procActionSwitch[elem])

  dpElems.append(p.getSoftware().getName()) 
  #dpElems.append(p.getSoftware().getVersion())
  #TODO inputfile 
  #not found in DataProcessing
  datatimestr = p.getCompletionTime().getDate() + p.getCompletionTime().getTime() # "," + p.getCompletionTime().getTime()
  dpElems.append(datatimestr)

  procAct = p.getProcessingActions()
  for elem in procAct:
    #print(procActionSwitch[elem])
    dpElems.append(procActionSwitch[elem])


print(dpElems)



## export routine to save as csv
## files: dataproc.csv
with open('dataproc.csv', 'wb') as dataprocfile:
  dataprocwriter = csv.writer(dataprocfile, delimiter="\t", lineterminator='\n')
  dataprocfile.write("ID\tSOFTWARE\tDATATIME\tACTIONS\n")
  dataprocfile.write('\t'.join(dpElems) + '\n')

'''
## database handling
con = sqlite3.connect(":memory:")
cur = con.cursor()
cur.execute("CREATE TABLE t (col1, col2);") # use your column names here

with open('dataproc.csv','rb') as fin: # `with` statement available in 2.5+
    # csv.DictReader uses first line in file for column headings by default
    dr = csv.DictReader(fin, delimiter='\t') # comma is default delimiter
    to_db = [(i['col1'], i['col2'], i['col3'], i['col4']) for i in dr]

cur.executemany("INSERT INTO t (col1, col2, col3, col4) VALUES (?, ?, ?, ?);", to_db)
con.commit()
con.close()

'''


conn = sqlite3.connect('quantitative.db')
c = conn.cursor()


sqlcreateTableElements = []
tablecolumnlabel = ["ID", "SOFTWARE", "DATATIME", "ACTIONS"]
tablecolumntype = ["text" ,"text" ,"text" , "text"]

for elem, s in enumerate(tablecolumnlabel):
  sqlcreateTableElements.append(tablecolumnlabel[elem]  + " " + tablecolumntype[elem])   
textinsert = (', '.join(sqlcreateTableElements))
print(sqlcreateTableElements)
executeString = "CREATE TABLE dataproc (" + textinsert + ");"
print(executeString)


c.execute(executeString)
#c.execute("CREATE TABLE dataproc (ID text, SOFTWARE text, DATATIME text, ACTIONS text);")



with open('dataproc.csv', 'rb') as dataprocfile:
  dr = csv.DictReader(dataprocfile, delimiter='\t')
  to_db = [(i["ID"],\
            i["SOFTWARE"],\
            i["DATATIME"],\
            i["ACTIONS"]) \
              for i in dr]

c.executemany("INSERT INTO dataproc \
  (ID,SOFTWARE,DATATIME,ACTIONS) VALUES (?, ?, ?, ?);", to_db)
conn.commit()
conn.close()





'''

#stubs 


conn = sqlite3.connect('dataProc.db')
#print("Opened database successfully")

c = conn.cursor()


c.execute("CREATE TABLE dataproc (id text, software text, datatime text);")
#for item in dpElems:
c.execute('insert into dataproc values (?,?,?)', dpElems)
#cursorObj.execute("INSERT INTO dataproc (id, software, datatime) VALUES (?,?,?);", dpElems)
#c.execute("CREATE TABLE  (ID integer,Feature_ref integer,RT real);")

'''