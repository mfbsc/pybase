#importFeatureMap
#read and store features from sqlite in featureXML (FeatureMap) format

#libs
from pyopenms import *
import csv
import itertools
import os
import sqlite3
import enum


## read FeatureMap
features = FeatureMap()
filehandle = FeatureXMLFile()

#fh.load("output.featureXML", features)
#filehandle.load(indexedFiles[1], features)


## connect to database
#create db connection
def create_connection(db_file):
  try:
    conn = sqlite3.connect(db_file)
    return conn
  except Error as e:
    print(e)
  return None




def main():
  database = "quantitative.db"
  conn = create_connection(database)
  cur = conn.cursor()
  cur.execute("SELECT * FROM dataproc")



## fill featureXML (FeatureMap) with quantitative.db information 
#dataProcessing
#features
#subordinates


##