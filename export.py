##
## ----------------------------------------------------------------------------
## $Maintainer: Matthias Fuchs$
## $Authors: Mattias Fuchs$
## ----------------------------------------------------------------------------

#exportFeatureTable
#read and store features from FeatureMap in csv format

#libraries
from pyopenms import *
from urllib import urlretrieve  # use this code for Python 2.x

import csv
import itertools
import os
import sqlite3
import enum


## functions

# check feature and userparameter entries for duplicate entries, mark userparameters labels with prefix '_'
def duplicateFinder(feature_Elements, userparams_elements):
  duplicates = []
  feature_Elements_set = set(feature_Elements)
  userparams_elements_set = set(userparams_elements)
  if (feature_Elements_set & userparams_elements_set):
    duplicates = list(feature_Elements_set & userparams_elements_set)
  for elem,s in enumerate(userparams_elements):
    if s in duplicates:
      userparams_elements[elem] = "_" + userparams_elements[elem]
  return userparams_elements


# convert csv_label_type suffix into fitting csv labels and types
# To Do: exchange type query method with valueType method in pyOpenMS library 
def prefixLabel(csv_label_type):
  table_column_label = []
  table_column_type  = []
  for elem in csv_label_type:
    if elem == 'int':
      table_column_label.append("")
      table_column_type.append("integer")  
    elif elem == 'float':
      table_column_label.append("")
      table_column_type.append("real")
    elif elem == 'str':
      table_column_label.append("")
      table_column_type.append("text")
    elif elem == 'list':
      # as agreed upon UserParams get prefixed column name and string type (text)
      if (elem.__class__.__name__) == 'int':
        table_column_label.append("_IL_")
        table_column_type.append("text") 
      elif (elem.__class__.__name__) == 'float':
        table_column_label.append("_FL_")
        table_column_type.append("text")
      elif (elem.__class__.__name__) == 'str':
        table_column_label.append("_SL_")
        table_column_type.append("text")
    #change   
    else:
      print("type error")
      print(elem)
  return table_column_label, table_column_type


def formatSQLEntries(elements, elements_types): #subordinate_userparam_elements, userparams_elements_types):
# construct table entries from combined subordinate and userparameter elements
# add prefixes for naming convention 
# return table entries and types respectively 
# combine feature/subordinate elements with userparameter elements
# concatenate pre-, suffixes if applicable 
  dynamic_column_prefixes, dynamic_column_types = prefixLabel(elements_types)

  sql_column_types_prefixes = subordinate_elements_type_prefixes + dynamic_column_prefixes
  sql_column_types = subordinate_elements_type + dynamic_column_types

  sql_header = []
  sql_table_elements = []
  sql_header_types = sql_column_types

  for elem, s in enumerate(elements):
    sql_header.append(sql_column_types_prefixes[elem] + elements[elem])
  return sql_header, sql_header_types



def createSQLTable(sql_header, sql_header_types, csv_file, db_filename):
  f = open(csv_file, 'rU')
  reader = csv.reader(f, delimiter = '\t')
  
  conn = sqlite3.connect(db_filename)
  c = conn.cursor()

  table_string = []
  for elem,s in enumerate(sql_header):
    table_string.append(sql_header[elem] + " " + sql_header_types[elem])
    
  table_string = (', '.join(table_string))
  create_table_string = "CREATE TABLE subordinates (" + table_string + ");"
  c.execute(create_table_string)

  dynamic_values = "INSERT INTO subordinates (" + \
                       str(', '.join(sql_header)) + \
                       ") VALUES (" + \
                       str("?," * (len(sql_header)-1)) + "?" + \
                       ");"

  for line in reader:
    c.execute(dynamic_values, tuple(line))

  conn.commit()
  conn.close()


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



#dpo = features.getDataProcessing()


# Todo without loops
# get labels for first column description
#for feature in itertools.islice(features, 0, 1):
#  print(feature.getRT())
#  k = []  # start with empty list to fill with key-value pairs
#  feature.getKeys(k) # explore available key-value pairs
#  for userparam in k:


# define parameters and types to export to csv
feature_elements = ["ID", "RT", "MZ", "Intensity", "Charge", "Quality"] 
feature_elements_type = ["integer", "real", "real", "real", "integer", "real"]
feature_elements_type_prefixes = ["", "", "", "", "", ""]


subordinate_elements = ["ID", "Feature_ref", "RT", "MZ", "Intensity", "Charge", "Quality"] 
subordinate_elements_type = ["integer", "integer", "real", "real", "real", "integer", "real"]
subordinate_elements_type_prefixes = ["", "", "", "", "", "", ""]



##################################################################################################
#
#                         subordinate csv and table creation in quantitative.db                
#
##################################################################################################

with open('subordinates.csv', 'wb') as subordinatefile:
  subordinatewriter = csv.writer(subordinatefile, delimiter='\t', lineterminator='\n')

  # subordinate file with userparameters
  userparams_elements_values = []
  row_counter = 0

  for feature in features:    
    if feature.getSubordinates():
      subordinates = feature.getSubordinates()
      for subordinate in subordinates:
        subordinate_elements_values = (subordinate.getUniqueId(), feature.getUniqueId() , subordinate.getRT(), subordinate.getMZ() , subordinate.getIntensity(), subordinate.getCharge(), subordinate.getOverallQuality())
        userparams_elements_values = []
        userparams_elements_values.extend(list(subordinate_elements_values))
        
        userparams_elements_types = []
        userparams_elements = []

        key_sub = []
        subordinate.getKeys(key_sub)        
        for userparam in key_sub:
          userparam_element = subordinate.getMetaValue(userparam)
          # construct list of userparam values and types
          userparams_elements_types.append(userparam_element.__class__.__name__)     
          userparams_elements.append(userparam) 
          userparams_elements_values.append(userparam_element)

        if row_counter == 0:          
          row_counter = 1
          #write header row to file
          #check for duplicates in subordinate_Elements and userparams_Elements
          userparams_elements = duplicateFinder(subordinate_elements, userparams_elements)
          subordinate_userparam_elements = subordinate_elements + userparams_elements
          subordinatefile.write('\t'.join(subordinate_userparam_elements) + '\n')
          subordinatewriter.writerow(userparams_elements_values)
        else:
          subordinatewriter.writerow(userparams_elements_values)


sql_header, sql_header_types = formatSQLEntries(subordinate_userparam_elements, userparams_elements_types)
createSQLTable(sql_header, sql_header_types, "subordinates.csv", "quantitative.db")
