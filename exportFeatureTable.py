#exportFeatureTable
#read and store features from FeatureMap in csv format

#libs
import csv
import itertools
import os
import sqlite3

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
#1st sanity check
print("Found " + str(features.size()) + " features")
#store in separate file as backup?
#FeatureXMLFile().store("test.out.featureXML", features)
##preliminary output to console
### user params


'''
#print(type(features))
fdp = features.getDataProcessing()
print(type(fdp))
print(fdp.getSoftware())

# Todo without loops
# get labels for first column description
#for feature in itertools.islice(features, 0, 1):
#  print(feature.getRT())
#  k = []  # start with empty list to fill with key-value pairs
#  feature.getKeys(k) # explore available key-value pairs
#  for userparam in k:
'''





# define parameter strings to export to csv
feature_Elements = ["ID", "RT", "MZ", "Intensity", "Charge", "Quality"] 
subordinate_Elements = ["ID", "Feature_ref", "RT", "featureMZ", "Intensity", "Charge", "Quality"] 

## export routine to save as csv
## files: feature.csv, subordinate.csv
with open('feature.csv', 'wb') as featurefile:
  featurewriter = csv.writer(featurefile, delimiter="\t", lineterminator='\n')
  #featurefile.write("feature Id \t\t\t\t  RT value \t\t\t\t  MZ ratio \t\t\t\t  Intensity \t\t Charge \t\t Quality \t\t" + '\n')
  #loop across features

  # feature file with parameters
  row_counter = 0
  for feature in itertools.islice(features, 0, 1):
  #for feature in features:
    currentrow = []
    feature_userparams_labels = []
    featureselect = (feature.getUniqueId(), feature.getRT(), feature.getMZ() , feature.getIntensity(), feature.getCharge(), feature.getOverallQuality())

    key = []
    feature.getKeys(key)  #populate key

    # build list of current row with featureselect and userparams
    currentrow.extend(list(featureselect))
    cnt = 1
    for userparam in key:
      feature_userparams_labels.append(userparam) 
      currentrow.append(feature.getMetaValue(userparam))
      #write header row to file
      feature_param_Elements = feature_Elements + feature_userparams_labels

    if row_counter == 0:
      row_counter = 1
      featurefile.write('\t'.join(feature_param_Elements) + '\n')
      featurewriter.writerow(currentrow)
      #print(len(currentrow))

    else:
      #print(len(currentrow))
      featurewriter.writerow(currentrow)



with open('subordinate.csv', 'wb') as subordinatefile:
  subordinatewriter = csv.writer(subordinatefile, delimiter='\t', lineterminator='\n')
  # subordinate file with parameters
  currentrow = []
  row_counter = 0
  #subord_userparams_labels = []
  #for feature in itertools.islice(features, 0, 1):
  for feature in features:
    #subordinate_userparams_labels = subordinate_Elements
    
    if feature.getSubordinates():
      subordinates = feature.getSubordinates()
      #currentrow = []
      for subordinate in subordinates:
        currentrow = []
        subordinate_userparams_labels = []
        key_sub = []

        subordinateselect = (subordinate.getUniqueId(), feature.getUniqueId() , subordinate.getRT(), subordinate.getMZ() , subordinate.getIntensity(), subordinate.getCharge(), subordinate.getOverallQuality())
        currentrow.extend(list(subordinateselect))
        
        subordinate.getKeys(key_sub)

        
        typeValue = []
        for userparam in key_sub:
          # playtime
          test = subordinate.getMetaValue(userparam)
          #test = feature.getMetaValue(userparam)
          #test1 = feature.valueType()
          #print(test1)
          #print(str(test))
          #print(type(test))
          #if (type(test) is float):
          #  print("float")
          #print(test.__class__.__name__)
          
          typeValue.append(test.__class__.__name__)     
          #typeofpara = test.valueType()

          subordinate_userparams_labels.append(userparam) 
          currentrow.append(subordinate.getMetaValue(userparam))

        if row_counter == 0:          
          row_counter = 1
          #print(subordinate_Elements)
          #write header row to file
          subordinate_param_Elements = subordinate_Elements + subordinate_userparams_labels
          subordinatefile.write('\t'.join(subordinate_param_Elements) + '\n')

          subordinatewriter.writerow(currentrow)
        else:
          subordinatewriter.writerow(currentrow)
        #print(len(subordinate_userparams_labels))

        #print(typeValue)


## database handling


conn = sqlite3.connect('quantitative.db')
#conn = sqlite3.connect(":memory:")
print("Opened database successfully")

c = conn.cursor()



tablecolumnlabel = []
tablecolumntype  = []
sqlcreateTableElements = []

for elem in typeValue:
  if elem == 'integer':
    #print("integer")
    tablecolumnlabel.append("")
    tablecolumntype.append("integer")  
  elif elem == 'float':
    #print("float")
    tablecolumnlabel.append("")
    tablecolumntype.append("real")
  elif elem == 'str':
    #print("text")
    tablecolumnlabel.append("")
    tablecolumntype.append("text")
  elif elem == 'IntegerList':
    #print("integer")
    tablecolumnlabel.append("_IL_")
    tablecolumntype.append("text")  
  elif elem == 'FloatList':
    #print("float")
    tablecolumnlabel.append("_FL_")
    tablecolumntype.append("real")
  elif elem == 'StringList':
    #print("text")
    tablecolumnlabel.append("_SL_")
    tablecolumntype.append("text")
  else:
    print("type error")


#print(tablecolumnlabel)
#print(tablecolumntype)
print("\n")
#print(tablecolumntype)
#print(subordinate_Elements)
subordinate_Elements_type = ["integer", "integer", "real", "real", "real", "integer", "real"]
subordinate_Elements_type_prefixes = ["", "", "", "", "", "", ""]

#tablecolumnlabel = ["_SL_","","","","","","","_IL_","","","","","_FL_","",""]
subordinate_Elements_type_prefixes += tablecolumnlabel


sqlcolumntype = subordinate_Elements_type + tablecolumntype
#print(sqlcolumntype)
print("imhere")
#print(subordinate_param_Elements)

for elem, s in enumerate(sqlcolumntype):
  #print(elem)
  #print(s)
  #print(subordinate_param_Elements[elem])
  #sqlcreateTableElements.append(subordinate_param_Elements[elem]  + " " + sqlcolumntype[elem])   
  sqlcreateTableElements.append(subordinate_Elements_type_prefixes[elem] + subordinate_param_Elements[elem]  + " " + sqlcolumntype[elem])   
  
print(sqlcreateTableElements)
print(', '.join(sqlcreateTableElements))
textinsert = (', '.join(sqlcreateTableElements))
print("\n")

print(textinsert)
executeString = "CREATE TABLE features (" + textinsert + ");"

print(type(executeString))
print("\n")
print(executeString)


c.execute(executeString)
#c.execute("CREATE TABLE features (ID integer,Feature_ref integer,RT real,MZ real,Intensity real,Charge	integer,Quality real,MZ1	real,peak_apex_position real,native_id text,peak_apex_int real,total_xic real,width_at_50 real,logSN real,isotope_probability real);")



with open('subordinate.csv', 'rb') as subordinatefile:
  dr = csv.DictReader(subordinatefile, delimiter='\t')
  to_db = [(i['ID'],\
            i['Feature_ref'],\
            i['RT'],\
            i['featureMZ'],\
            i['Intensity'],\
            i['Charge'],\
            i['Quality'],\
            i['MZ'],\
            i['peak_apex_position'],\
            i['native_id'],\
            i['peak_apex_int'],\
            i['total_xic'],\
            i['width_at_50'],\
            i['logSN'],\
            i['isotope_probability'],\
  ) for i in dr]

c.executemany("INSERT INTO features \
  (ID,\
   Feature_ref,\
   RT,\
   featureMZ,\
   Intensity,\
   Charge,\
   Quality,\
   MZ,\
   peak_apex_position,\
   native_id,\
   peak_apex_int,\
   total_xic,\
   width_at_50,\
   logSN,\
   isotope_probability\
  ) VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", to_db)
conn.commit()
conn.close()


