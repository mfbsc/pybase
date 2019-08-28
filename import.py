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


##libraries
from pyopenms import *

import csv
import itertools
import os
import sqlite3
import enum
import pyopenms as pms



## connect to database
#create db connection
def create_connection(db_file):
  try:
    connection = sqlite3.connect(db_file)
    return connection
  except Error as e:
    print(e)
  return None

'''
def copyDBToRAM(source_connection, dbname=':memory:'):
  #Return a connection to a new copy of an existing database.                        
  #Raises an sqlite3.OperationalError if the destination already exists.             
  
  #SQLITE 3.6.11 new in 3.7
  #source = sqlite3.connect('quantitative.db')
  #destination = sqlite3.connect(':memory:')
  #source.backup(destination)
  script = ''.join(source_connection.iterdump())
  dest_conn = sqlite3.connect(dest_dbname)
  dest_conn.executescript(script)
  return dest_conn
'''


def copyDatabaseToRAM(source_connection):
  #Return a connection to a new copy of an existing database.                        
  #Raises an sqlite3.OperationalError if the destination already exists.             
  
  script = ''.join(source_connection.iterdump())
  dest_conn = sqlite3.connect(":memory:")
  dest_conn.executescript(script)
  return dest_conn



#def readTables(connection):
#  cursor = connection.cursor()

def getTableNames(connection):
  connection.text_factory = str #return text data type
  cursor = connection.cursor()
  cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
  tables = cursor.fetchall()

  return tables

def readTableTuple(connection, table_name):
  cursor = connection.cursor()
  cursor.execute("SELECT * FROM " + table_name)
  rows = cursor.fetchall()

  #return table = cursor.fetchall()


def main():
  database_filename = "quantitative.db"
  conn_db = create_connection(database_filename)
  conn_mem = copyDatabaseToRAM(conn_db)
  conn_mem.text_factory = str

  tables = getTableNames(conn_mem)
  
  #ar = [[str(item) for item in results] for results in tables] # for byte mode instead of text_factory
  #print(ar[2][0])

  #print(tables[2][0])

  table_dict = {}

  for elem in tables:
     # start populating FeatureXML files with values of corresponding tables
    print(elem[0])
    table_dict[elem] = readTableTuple(conn_mem, elem[0])

  
  #print(len(table_dict[]))
  for key in table_dict:
    print(type(key))

#    "tuple" + str(elem[0]) = readTableTuple(conn_mem, elem[0])
  conn_mem.close()

if __name__ == '__main__':
  main()




'''


  for row in rows[1:-2]:
    #print(type(row))
    print(row)
    teststring = row[0]
    table_list.append(row)

  table_list = []





# zetcode.com/db/sqlitepythontutorial/
# fetchall returns tuple of tuples (features x rows)
# first row still contains header and headertypes
rows = cur.fetchall()


for row in rows[1:-2]:
  print(type(row))
  print(row)
  teststring = row[0]
  table_list.append(row)


conn.close()




print(len(table_list))
print(table_list)







conn = create_connection(database_file)

with open("dump.sql", "w") as f:
  for line in conn.iterdump():
    f.write('%s\n' % line)
conn.close





'''



#dataproc = features.
#features.DataProcessing.setCompletionTime(rows[2])


'''


## read FeatureMap
features = FeatureMap()
filehandle = FeatureXMLFile()


## fill featureXML (FeatureMap) with quantitative.db information 
#dataProcessing
#features
#subordinates


## read FeatureMap
fmap = FeatureMap()
features = FeatureMap()
smallfeature = FeatureMap()








#print(teststring)
print(type(teststring))
print(teststring)

feature_handle = 


# thanks to sneumann FeatureFinderCentroided.py uwe schmitts test000.py

features = pms.FeatureMap()

test = ("12321143421312")

test = features.setUniqueId(12332132133213321)
features.setFeatures()

#features.push_back()

features.

#addDataProcessing(features, params, pms.ProcessingAction.QUANTITATION)

#fh = pms.FeatureXMLFile()
#fh.store("import.featureXML", features)



FeatureXMLFile().store("import.featureXML", features)


#1st sanity check
print("Found " + str(features.size()) + " features")




## TODO activate as script method if completed
#def main():
#  # run functions and extraneous code

#if __name__ == "__main__":
#  main()
'''