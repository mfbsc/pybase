##
## ----------------------------------------------------------------------------
## $Maintainer: Matthias Fuchs$
## $Authors: Mattias Fuchs$
## ----------------------------------------------------------------------------

#exportFeatureTable
#read and store features from FeatureMap in csv format
#and export to sql tables features, subordinates and dataprocessing

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
def duplicateFinder(feature_elements, userparams_elements):
  duplicates = []
  feature_elements_set = set(feature_elements)
  userparams_elements_set = set(userparams_elements)
  if (feature_elements_set & userparams_elements_set):
    duplicates = list(feature_elements_set & userparams_elements_set)
  for elem,s in enumerate(userparams_elements):
    if s in duplicates:
      userparams_elements[elem] = "_" + userparams_elements[elem]
  return userparams_elements

# convert csv_label_type suffix into fitting csv labels and types
# To Do: exchange type query method with valueType method in pyOpenMS library (not implmented)
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

# construct table entries from combined subordinate and userparameter elements
# add prefixes for naming convention 
# return table entries and types respectively 
# combine feature/subordinate elements with userparameter elements
# concatenate pre-, suffixes if applicable 
def formatSQLEntries(elements, elements_types, elements_type, elements_types_prefixes): 

  dynamic_column_prefixes, dynamic_column_types = prefixLabel(elements_types)

  sql_column_types_prefixes = elements_types_prefixes + dynamic_column_prefixes
  sql_column_types = elements_type + dynamic_column_types

  sql_header = []
  sql_table_elements = []
  sql_header_types = sql_column_types

  for elem, s in enumerate(elements):
    sql_header.append(sql_column_types_prefixes[elem] + elements[elem])
  return sql_header, sql_header_types

# builds tables of header, header types, a csv as input and the database name 
def createSQLTable(sql_header, sql_header_types, csv_file, db_filename):
  f = open(csv_file, 'rU')
  filename = csv_file.split(".")
  filename = filename[0]
  reader = csv.reader(f, delimiter = '\t')
  
  conn = sqlite3.connect(db_filename)
  c = conn.cursor()

  table_string = []
  for elem,s in enumerate(sql_header):
    table_string.append(sql_header[elem] + " " + sql_header_types[elem])

  table_string = (', '.join(table_string))
  create_table_string = "CREATE TABLE "+ filename +" (" + table_string + ");"
  c.execute(create_table_string)

  dynamic_values = "INSERT INTO "+ filename +" (" + \
                       str(', '.join(sql_header)) + \
                       ") VALUES (" + \
                       str("?," * (len(sql_header)-1)) + "?" + \
                       ");"

  counter = 0
  for line in reader:

    counter += 1
    c.execute(dynamic_values, tuple(line))

  conn.commit()
  conn.close()


def main():
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
  valueOfFileIndex = input("Enter featureXML index: ") - 1
  print('File selection: ' + indexedFiles[valueOfFileIndex] + '\n')

  ## read FeatureMap
  features = FeatureMap()
  filehandle = FeatureXMLFile()

  #fh.load("output.featureXML", features)

  ## changed for testing purposes
  filehandle.load(indexedFiles[valueOfFileIndex], features)
  #filehandle.load(indexedFiles[1], features)
  #1st sanity check
  print("Found " + str(features.size()) + " features")
  #store in separate file as backup?
  #FeatureXMLFile().store("test.out.featureXML", features)
  ##preliminary output to console
  ### user params




  # Todo without loops
  # get labels for first column description
  #for feature in itertools.islice(features, 0, 1):
  #  print(feature.getRT())
  #  k = []  # start with empty list to fill with key-value pairs
  #  feature.getKeys(k) # explore available key-value pairs
  #  for userparam in k:

  empty_elements_switcher = {
    'int' : 0,   
    'float' : 0.0,
    'list' : '[]',
    'str' : ' '
  }

  # define parameters and types to export to csv
  feature_elements = ["ID", "RT", "MZ", "Intensity", "Charge", "Quality"] 
  feature_elements_types = ["integer", "real", "real", "real", "integer", "real"]
  feature_elements_types_preSQL = ["int", "float", "float", "float", "int", "float"]
  feature_elements_types_prefixes = ["", "", "", "", "", ""]


  subordinate_elements = ["ID", "Feature_ref", "RT", "MZ", "Intensity", "Charge", "Quality"] 
  subordinate_elements_types = ["integer", "integer", "real", "real", "real", "integer", "real"]
  subordinate_elements_types_preSQL = ["int", "int", "float", "float", "float", "int", "float"]
  subordinate_elements_types_prefixes = ["", "", "", "", "", "", ""]

  ## database handling
  conn = sqlite3.connect('quantitative.db')
  #conn = sqlite3.connect(":memory:")
  print("Opened database successfully")
  c = conn.cursor()


  # clear existing table
  c.execute("DROP TABLE IF EXISTS features")
  c.execute("DROP TABLE IF EXISTS subordinates")
  c.execute("DROP TABLE IF EXISTS dataproc")



  ##################################################################################################
  #                         feature csv and table creation in quantitative.db                
  ##################################################################################################
  # feature file with parameters
  ## export routine to save as csv
  ## files: feature.csv

  with open('features.csv', 'wb') as featurefile:
    featurewriter = csv.writer(featurefile, delimiter="\t", lineterminator='\n')
    
    # feature file with parameters
    row_counter = 0

    userparams_elements_old = []  ################################################
    counter_empty_list = 0
    empty_elements_list = []


    for feature in features:
      # initialize list for current row entries 
      currentrow = []
      userparams_elements = []
      feature_userparam_elements = []
      featureselect = (feature.getUniqueId(), feature.getRT(), feature.getMZ() , feature.getIntensity(), feature.getCharge(), feature.getOverallQuality())

      subordinate_param_Elements = []
      key = []
      feature.getKeys(key)  #populate key

      # build list of current row with featureselect and userparams for csv file
      currentrow.extend(list(featureselect))
      userparams_elements_types = []

      for userparam in key:
        #get label type of userparam
        meta_value = feature.getMetaValue(userparam)
        #print(str(type(test_feat)) + "\n")

        #populate userparameter value type list
        userparams_elements_types.append(meta_value.__class__.__name__)     

        #populate header row of csv file
        userparams_elements.append(userparam)

        #if(test_feat.__class__.__name__ == 'list'):
        #  print("test auf list element")
        #  print(str(feature.getMetaValue(userparam)))
        #  currentrow.append(str(feature.getMetaValue(userparam)))
        #else:
        currentrow.append(meta_value)

      userparams_elements_new = userparams_elements     ################################################
      #print(len(currentrow))
      if ((len(userparams_elements_new) != len(userparams_elements_old)) and userparams_elements_old):
        uen_set = set(userparams_elements_new)
        ueo_set = set(userparams_elements_old)
        empty_elements = list(ueo_set - uen_set)
        #print("\n")
        #index_matches = [i for i, x in enumerate(header) if x in empty_elements]  
        #print(index_matches)

        #for loop
        empty_elements_list = []
        for index, elem in enumerate(header):
          if elem in empty_elements:
            #print(elem, index)
            empty_elements_list.append([elem, index])
        #print(empty_elements_list)
      userparams_elements_old = userparams_elements_new  ################################################

      
      if row_counter == 0:
        row_counter = 1

        #concatenate feature elements with userparams to build header row of csv file 
        feature_userparam_elements = feature_elements + userparams_elements
        featurefile.write('\t'.join(feature_userparam_elements) + '\n')

        header = feature_userparam_elements
        header_types = userparams_elements_types



        ##########################################
        #print(len(currentrow))
        featurewriter.writerow(currentrow)
        #print(header_types)
        #print(len(header_types))       
        header_list_types = feature_elements_types_preSQL + header_types
        #print(header_list_types)
        #print(currentrow)
        
        empty_elements_list_types = []
        counter_empty_list +=1
        for item in header_list_types:
          #if item in empty_elements_switcher:
          empty_elements_list_types.append(empty_elements_switcher.get(item))
            
          #empty_elements_list_types.append(item in empty_elements_switcher)
        #  if item in empty_elements_switcher:



      else:
        #print(len(currentrow))
        # implement multiple value exception
        if(empty_elements_list): ################################################
          #currentrow.insert(empty_elements_list[0][1], " ")
          #print(empty_elements_list[0][1])
          index = empty_elements_list[0][1]
          #currentrow.insert(14, " ")    ############################### insert value according to type
          currentrow.insert(index, empty_elements_list_types[index])
        featurewriter.writerow(currentrow)

  #print(empty_elements_list_types)
  #print(counter_empty_list)
  
  
  # must be in feature_writer
  # insert working
  # adapt insert to corresponding correct type?
  # add two type lists together in order to write into csv file empty_list_elements 
  # feature_elements_types + header_types
  #
  #
  #
  #
  #
  #
  #
  #
  #
  #
  #


  ## feature table
  #print(len(header_types))
  sql_header, sql_header_types = formatSQLEntries(header, header_types, feature_elements_types, feature_elements_types_prefixes)
  #print(sql_header_types)
  createSQLTable(sql_header, sql_header_types, "features.csv", "quantitative.db")



  ##################################################################################################
  #                         subordinate csv and table creation in quantitative.db                
  ##################################################################################################

  with open('subordinates.csv', 'wb') as subordinatefile:
    subordinatewriter = csv.writer(subordinatefile, delimiter='\t', lineterminator='\n')

    # subordinate file with userparameters
    userparams_elements_values = []
    subordinate_userparam_elements = []
    row_counter = 0
    subordinates_boolean = False

    for feature in features:  
      subordinates_boolean = feature.getSubordinates()  
      if subordinates_boolean: #feature.getSubordinates():
        subordinates = feature.getSubordinates()
        print(type(subordinates))
        print(subordinates[0])
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
            #print(len(subordinate_elements))
            #print(len(userparams_elements))
            subordinate_userparam_elements = subordinate_elements + userparams_elements
            subordinatefile.write('\t'.join(subordinate_userparam_elements) + '\n')
            subordinatewriter.writerow(userparams_elements_values)
          else:
            subordinatewriter.writerow(userparams_elements_values)


  if subordinates_boolean:
    sql_header, sql_header_types = formatSQLEntries(subordinate_userparam_elements, userparams_elements_types, subordinate_elements_types, subordinate_elements_types_prefixes)  
    createSQLTable(sql_header, sql_header_types, "subordinates.csv", "quantitative.db")




  
  dataproc = features.getDataProcessing()

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

  dataproc_elems = []
  dataproc_elems.append(str(features.getUniqueId()))

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

  with open('dataproc.csv', 'wb') as dataprocfile:
    dataprocwriter = csv.writer(dataprocfile, delimiter="\t", lineterminator='\n')
    dataprocfile.write("ID\tSOFTWARE\tDATA\tTIME\tACTIONS\n")
    dataprocfile.write('\t'.join(dataproc_elems) + '\n')

  conn = sqlite3.connect('quantitative.db')
  c = conn.cursor()

  sqlcreateTableElements = []
  sql_header = ["ID", "SOFTWARE", "DATE", "TIME", "ACTIONS"]
  sql_header_types = ["integer" ,"text" ,"text" ,"text" , "text"]

  createSQLTable(sql_header, sql_header_types, "dataproc.csv", "quantitative.db")




if __name__ == '__main__':
  main()