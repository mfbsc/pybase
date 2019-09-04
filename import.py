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
def setFeature(input_from_lines):
  feature = Feature()
  #for element in input_from_lines:
    
    #lookup function in dictionary and execute
    #ideas for improvement?

  return feature

#store feature 
def storeFeature(feature, feature_map):
  feature_map.push_back(feature)
  return feature_map


#function definitions of labels
def getUniqueId(int_nr):
  return str(int_nr)

def setParentId(int_nr):
  return str(int_nr)

def setRT(int_nr):
  return str(int_nr)

def setMZ(double_nr):
  return str(double_nr)

def setIntensity(double_nr):
  return str(double_nr)

def setCharge(int_nr):
  return str(int_nr)

def setOverallQuality(double_nr):
  return str(double_nr)

def dummy_func(input):
  return (input)

def labelToFunction(label_arg):
  function = label_switcher.get(label_arg)
  return function
 

##############################################################################
#                                 main                                       #
##############################################################################

def main():

  label_switcher = {
    'ID' : getUniqueId,   
    'Feature_ref' : setParentId, #(int),
    'RT' : setRT, #(double)
    'MZ' : setMZ, #(double),
    'Intensity' : setIntensity, #(double),
    'Charge' : setCharge, #(int),
    'Quality' : setOverallQuality, #(double),
    '_MZ' : dummy_func,
    'native_id' : dummy_func,
    'peak_apex_position' : dummy_func,
    'peak_apex_int' : dummy_func,
    'total_xic' : dummy_func,
    'width_at_50' : dummy_func,
    'logSN' : dummy_func,
    'isotope_probability' : dummy_func
    } 

  #start of main
  database_filename = "quantitative.db"
  conn_db = create_connection(database_filename)
  conn_mem = copyDatabaseToRAM(conn_db)
  conn_mem.text_factory = str

  tables = getTableNames(conn_mem)
  table = readTableTuple(conn_mem, tables[2][0])

  # feature map instantiation
  fm = FeatureMap()
  
  '''
  #feature = Feature()
  
  # test values
  feature.setMZ(500.9)
  feature.setRT(1500.9)
  feature.setIntensity(509)
  feature.setOverallQuality(8)
  feature.setUniqueId(111334122223231411)
  fm.push_back(feature)
  '''

  table = readTableTuple(conn_mem, tables[2][0])
  header = getHeader(table)
  data = getData(table)

  '''
  for label in header:
    if label in label_switcher:
      print(label_switcher[label](5))
      #print(label_switcher[label])
  '''
  #print(data[0][:])


  #print(len(header))
  #print(len(data[0][:]))

  #for line in data:  # walk across labels and line elements to create featureXML entries 
  for (label,value) in itertools.izip_longest(header,data[0][:]):
    if label in label_switcher:
      #print label, value
      print(label_switcher[label](value))
      #print(label_switcher[label])
  
  '''

  #func = label_switcher.get(argument, 4)
  print(label_switcher['ID'](5))
  #print(func())
  #exec(func)
  '''  










  # ensure uniqueness of ids
  fm.ensureUniqueId()
  FeatureXMLFile().store("test.featureXML", fm)


  '''
  x = []
  for line in table[0:1]:
    print(line)                              # print line in current table
    for item in line:
      if item in label_switch:
        x.append(item)
  '''  


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







'''
# zetcode.com/db/sqlitepythontutorial/
# fetchall returns tuple of tuples (features x rows)
# first row still contains header and headertypes
rows = cur.fetchall()

for row in rows[1:-2]:
  print(type(row))
  print(row)
  teststring = row[0]
  table_list.append(row)

'''

## fill featureXML (FeatureMap) with quantitative.db information 
#dataProcessing
#features
#subordinates

def populateFeatureXML(table):
  #1. read in datatype by header tuple[0], check if underscores, these labels as subordinates
  #   if list of type _IL_ _SL_ _FL_ handle as string, integer as int, real as float, text as str
  #   cast, if necessary take look at functions
  #2. access corresponding list of tuples via loop
  #3. instantiate elements
  #4. write tables in order 1. dataproc 2. features 3. subordinates
  #   use dict as switch case for subordinate check
  #   use feature_id as reference to access subordinate tables (write tables as dictionaries for key retrieval?)
  #   
  print("guckguck")

  
'''
  feature_label_switch = {
    'ID' :  "getUniqueId(int)"   
    'RT' :  "setRT(double)",
    'MZ' :  "setMZ(double)",
    'Intensity' :  "setIntensity(double)",
    'Charge' :  "setCharge(int)",  
    'Quality' :  "setOverallQuality(double)",
    'label' :  
    'total_xic' :  
    'expected_rt' :  
    'PeptideRef' :  
    'leftWidth' :  
    'rightWidth' :  
    'peak_apices_sum' :  
    'masserror_ppm' :  
    'var_xcorr_coelution' :  
    'var_xcorr_coelution_weighted' :  
    'var_xcorr_shape' :  
    'var_xcorr_shape_weighted' :  
    'var_library_corr' :  
    'var_library_rmsd' :  
    'var_library_sangle' :  
    'var_library_rootmeansquare' :  
    'var_library_manhattan' :  
    'var_library_dotprod' :  
    'var_intensity_score' :  
    'nr_peaks' :  
    'sn_ratio' :  
    'var_log_sn_score' :  
    'var_elution_model_fit_score' :  
    'xx_lda_prelim_score' :  
    'var_isotope_correlation_score' :  
    'var_isotope_overlap_score' :  
    'var_massdev_score' :  
    'var_massdev_score_weighted' :  
    'var_bseries_score' :  
    'var_yseries_score' :  
    'var_dotprod_score' :  
    'var_manhatt_score' :  
    'main_var_xx_swath_prelim_score' :  
    'missedCleavages' :  
    'PrecursorMZ' :  
    'ms1_area_intensity' :  
    'ms1_apex_intensity' :  
    'xx_swath_prelim_score' :  
    'sum_formula' :  
    'rt_deviation' :  
    'model_height' :  
    'model_FWHM' :  
    'model_center' :  
    'model_lower' :  
    'model_upper' :  
    'model_Gauss_sigma' :  
    'model_error' :  
    'model_area' :  
    'model_status' :  
    'raw_intensity' :  
  } 


def label_switch(x):
  return {
    #'ID' : "getUniqueId(int)",   
    #'RT' : "setRT(double)",
    #'MZ' : "setMZ(double)",
    #'Intensity' : "setIntensity(double)",
    #'Charge' : "setCharge(int)",
    'Quality' : "2"
  }.get(x,"type not found")
'''

