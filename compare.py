#compare speed and size
#read and store features from sqlite in featuremap format

#libs
from pyopenms import *
import csv
import enum
import itertools
import os
import sqlite3
from time import *
import time
import timeit
import multiprocessing

## import featureXML, store as sqlite.db, reimport and store as featureXML 
## compare filesize, missing data and access speeds

# stackoverflow 7370801
#simple timeit
start = time.time() #time.process_time()
#run tasks
print("test")
end = time.time() #time.process_time()
diff = end - start
print("Elapsed time:", diff)
