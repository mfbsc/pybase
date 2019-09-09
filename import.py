##
## ----------------------------------------------------------------------------
## $Maintainer: Matthias Fuchs$
## $Authors: Mattias Fuchs$
## ----------------------------------------------------------------------------

#importFeatureMap
#read and store features from sqlite in featureXML (FeatureMap) format
#1. open database and return connection (selection function)
#2. read in tables
#3. save input to datastructure (list of tuples?, tuples of tuples)
#4. populate FeatureXMLFile() with value pairs (check for subordinates) of all tables (dataproc, features, subordinates)


## libraries
from pyopenms import *

import csv
import itertools
import os
import sqlite3
import enum
import numpy


## functions

#create database connection
def create_connection(db_file):
  try:
    connection = sqlite3.connect(db_file)
    return connection
  except Error as e:
    print(e)
  return None


#return connection to database in RAM .                        
def copyDatabaseToRAM(source_connection):
  script = ''.join(source_connection.iterdump())
  dest_conn = sqlite3.connect(":memory:")
  dest_conn.executescript(script)
  return dest_conn


#return table names in database 
#ar = [[str(item) for item in results] for results in tables] # for byte mode instead of text_factory
def getTableNames(connection):
  connection.text_factory = str #return text data type
  cursor = connection.cursor()
  cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
  tables = cursor.fetchall()
  return tables

#returns table as tuple with header and subsequent lines of data
def readTableTuple(connection, table_name):
  cursor = connection.cursor()
  cursor.execute("SELECT * FROM " + table_name)
  table = cursor.fetchall()
  return table

#return header line with element labels of db tables
def getHeader(table):
  return (table[0][:])

#return values of db table 
def getData(table):
  return (table[1:][:])

#read labels in header and convert to datatypes, set function call list
def setFunctionList(header):
  datatypes = []
  for element in header:
    # see export function of datatypes
    #dictionary_with_types # find key and return datatype
    datatypes.append() #append dictionary value of datatype
  return datatypes



#set feature with table values line
'''
def setFeature(input_from_lines):
  feature = Feature()
  #for element in input_from_lines:
    
    #lookup function in dictionary and execute
    #ideas for improvement?

  return feature
'''

#store feature 
def storeFeature(feature, feature_map):
  feature_map.push_back(feature)
  return feature_map

#function definitions of labels
def setUniqueId(feature, int_nr):
  return feature.setUniqueId(long(int_nr))

#def setParentId(int_nr):
#  return setParentId( int_nr)

def setRT(feature, int_nr):
  return feature.setRT(int_nr)

def setMZ(feature, double_nr):
  return feature.setMZ(double_nr)

def setIntensity(feature, double_nr):
  return feature.setIntensity(double_nr)

def setCharge(feature, int_nr):
  return feature.setCharge(int_nr)

def setOverallQuality(feature, double_nr):
  return feature.setOverallQuality(double_nr)

def setWidth(feature, double_nr):
  return feature.setWidth(double_nr)

def setMetaValue(feature, String, DataValue):
  return feature.setMetaValue(String, DataValue)

def dummy_func(feature, input):
  print(input)

  

def labelToFunction(label_arg):
  function = label_switcher.get(label_arg)
  return function
 

label_switcher = {
  'ID' : setUniqueId,   
  'Feature_ref' : setUniqueId, #(int), setParentId
  'RT' : setRT, #(double)
  'MZ' : setMZ, #(double),
  '_MZ' : setMZ, #(double),
  'Intensity' : setIntensity, #(double),
  'Charge' : setCharge, #(int),
  'Quality' : setOverallQuality, #(double),
  'width_at_50' : setWidth
}

fm = FeatureMap()

def setFeature(feature, header, data):
  for (label,value) in itertools.izip_longest(header,data):
    if label in label_switcher:
      label_switcher[label](feature, value)
    else:
      setMetaValue(feature, label, value)
  fm.push_back(feature)
  # ensure uniqueness of ids
  fm.ensureUniqueId()


##############################################################################
#                                 main                                       #
##############################################################################

def main():



  '''
    '_MZ' : dummy_func #, 
    'native_id' : dummy_func,
    'peak_apex_position' : setMetaValue,
    'peak_apex_int' : dummy_func,
    'total_xic' : dummy_func,
    'logSN' : dummy_func,
    'isotope_probability' : dummy_func
    } 
  '''

  #start of main
  database_filename = "quantitative.db"
  conn_db = create_connection(database_filename)
  conn_mem = copyDatabaseToRAM(conn_db)
  conn_mem.text_factory = str

  tables = getTableNames(conn_mem)
  table = readTableTuple(conn_mem, tables[1][0])

  # feature map instantiation
  #fm = FeatureMap()

  # set table by name 
  for index, elem in enumerate(tables):
    elem_string = elem[0]
    if elem_string == 'dataproc':
      table_dataproc = readTableTuple(conn_mem, tables[index][0])
    elif elem_string == 'features':
      table_features = readTableTuple(conn_mem, tables[index][0])
    elif elem_string == 'subordinates':
      table_subordinates = readTableTuple(conn_mem, tables[index][0])
    else:
      print("table not used yet")
      break


  '''
  ###############################################################################
  #                        write dataproc to featureXML                         #
  ###############################################################################
  '''
  
  '''
  # write dataproc to featureXML
  table_data_proc = readTableTuple(conn_mem, tables[0][0])
  header = getHeader(table_data_proc)
  data = getData(table_data_proc)
  '''
  

  ##### DataProcessing
  #fm.setDataProcessing(["test","test"])
  # set dataproc entries

  #dataproc = fm.setDataProcessing.setCompletionTime()
  #fm.DataProcessing.Software.setSoftware("test") #('1999-12-31')

  '''
  for p in dataproc:
    dataproc_elems.append(p.getSoftware().getName()) 
    #datastr = p.getCompletionTime().getDate()# + p.getCompletionTime().getTime() 
    datastr = p.getCompletionTime().getDate()# + p.getCompletionTime().getTime() 
    timestr = p.getCompletionTime().getTime() 
    #dataproc_elems.append(datatimestr)
    dataproc_elems.append(datastr)
    dataproc_elems.append(timestr)
    procAct = p.getProcessingActions()
    for elem in procAct:
      dataproc_elems.append(procActionSwitch[elem])
  '''



  ###############################################################################
  #                        write features to featureXML                         #
  ###############################################################################
  '''
  header_features = getHeader(table_features)
  data_features = getData(table_features)
  
  for line in data_features:
    feature = Feature()
    for (label,value) in itertools.izip_longest(header_features,line):
      if label in label_switcher:
        #print(label)
        label_switcher[label](feature, value)
      else:
        #print(label)
        #print(type(label))
        #print(value)
        setMetaValue(feature, label, value)
    #else:
    #  print(label)
    fm.push_back(feature)
    # ensure uniqueness of ids
    fm.ensureUniqueId()
  '''


  header_features = getHeader(table_features)
  data_features = getData(table_features)

  print(len(tables))

  if len(tables) >= 3:
    header_subordinates = getHeader(table_subordinates)
    data_subordinates = getData(table_subordinates)
    # contains list of feature ids with subordinates  
    subordinates_Ids = [int(row[1]) for row in data_subordinates]

    header_subordinates_list = header_subordinates[:1] + header_subordinates[2:]
  #data_subordinates_list = data_subordinates[:1] + data_subordinates[2:]
  

  # walk across all features
  # populate features
  # look for feature id in subordinate id
  # if in subordinate id construct subordinate feature and populate
  for feature_line in data_features:
    feature = Feature()
    setFeature(feature, header_features, feature_line)
    feature_id = int(feature_line[0])
    subord_list = []
    if len(tables) > 2:
      for subordinate_line in data_subordinates:
        if feature_id == int(subordinate_line[1]):
          subordinate = Feature()
          subord_line = subordinate_line[:1] + subordinate_line[2:]
          
          for (label,value) in itertools.izip_longest(header_subordinates_list,subord_line):
            if label in label_switcher:
              label_switcher[label](subordinate, value)
            else:
              setMetaValue(subordinate, label, value)
          #fm.push_back(subordinate)
          # ensure uniqueness of ids
          #fm.ensureUniqueId()
          subord_list.append(subordinate)
          print(len(subord_list))
          #feature.setSubordinates()
        feature.setSubordinates(subord_list)


      

      #print(header_subordinates_list[0])
      #print(int(subord_line[0]))
      #subordinate_feature = Feature()
      #setFeature(subordinate_feature, header_subordinates_list, subord_line)
      #feature.setSubordinates()




  '''
  ###############################################################################
  #                      write subordinates to featureXML                       #
  ###############################################################################
  header_subordinates = getHeader(table_subordinates)
  data_subordinates = getData(table_subordinates)

  #print(data_subordinates[0][1])
  #print(data_features[0][:])
  #print([int(row[0]) for row in data_features])
  features_Ids = [int(row[0]) for row in data_features]
  print(features_Ids)

  header_subordinates_list = header_subordinates[:1] + header_subordinates[2:]
  print(header_subordinates_list)
  #print(header_subordinates)

  
  #find entries in 2nd column of data_subordinates which correspoond
  #to feature_ref in data_features and add their corresponding subordinates
  #subordinates = feature.getSubordinates()
  
  for line in data_subordinates:
    #print(type(line))
    #print(line[1])
    if int(line[1]) in features_Ids:
      print("is in")
      print(line)
      subord_line = line[:1] + line[2:]
      print(subord_line)
      feature = Feature()
      for (label,value) in itertools.izip_longest(header_subordinates_list,subord_line):
        if label in label_switcher:
          #print(label)
          label_switcher[label](feature, value)
        else:
          #print(label)
          #print(type(label))
          #print(value)
          setMetaValue(feature, label, value)
            #  print(label)
      fm.push_back(feature)
      # ensure uniqueness of ids
      fm.ensureUniqueId()
  
  '''
  uniqueId = long(data_features[0][0])
  print(uniqueId)

  # set featuremap Id  
  fm.setUniqueId(uniqueId)





  FeatureXMLFile().store("test.featureXML", fm)
  

  '''
  for elem in table_dict[item][0]:
    print(elem)
    #if elem == "ID":
    if elem in label_switch:
      print(elem)
      print("true")

  feature = Feature()    
  table_dict = {}

  for elem in tables:
    # start populating FeatureXML files with values of corresponding tables
    #print(elem[0])
    table_dict[elem] = readTableTuple(conn_mem, elem[0])
    print(type(table_dict[elem]))
    print(len(table_dict[elem]))

  for item in table_dict:
    #print(type(item))
    #print(item[0], table_dict[item][0])     # 0 returns header of table
    for elem in table_dict[item][0]:
      print(elem)
      #if elem == "ID":
      if elem in label_switch:
        print(elem)
        print("true")
  '''

  


  # close database
  conn_mem.close()
  # end of main


# main call
if __name__ == '__main__':
  main()



#################################################  EOL  ###############################################



'''
# zetcode.com/db/sqlitepythontutorial/
# fetchall returns tuple of tuples (features x rows)
# first row still contains header and headertypes
rows = cur.fetchall()
'''

#dataProcessing
#features
#subordinates

#def populateFeatureXML(table):
  #1. read in datatype by header tuple[0], check if underscores, these labels as subordinates
  #   if list of type _IL_ _SL_ _FL_ handle as string, integer as int, real as float, text as str
  #   cast, if necessary take look at functions
  #2. access corresponding list of tuples via loop
  #3. instantiate elements
  #4. write tables in order 1. dataproc 2. features 3. subordinates
  #   use dict as switch case for subordinate check
  #   use feature_id as reference to access subordinate tables (write tables as dictionaries for key retrieval?)
  #   




  #find entries in 2nd column of data_subordinates which correspoond
  #to feature_ref in data_features and add their corresponding subordinates
  #subordinates = feature.getSubordinates()
