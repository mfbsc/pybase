#exportFeatureTable
#read and store features from FeatureMap in csv format

#libs
import csv
import itertools
import os

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
valueOfFileIndex = input("Enter featureXML index: ") - 1
print('File selection: ' + indexedFiles[valueOfFileIndex] + '\n')

## read FeatureMap
features = FeatureMap()
filehandle = FeatureXMLFile()
#fh.load("output.featureXML", features)
filehandle.load(indexedFiles[valueOfFileIndex], features)
#1st sanity check
print("Found " + str(features.size()) + " features")
#store in separate file as backup?
#FeatureXMLFile().store("test.out.featureXML", features)
##preliminary output to console


# define parameter strings to export to csv
feature_Elements = ["FeatureId", "RTvalue", "MZratio", "Intensity", "Charge", "Quality"] 
subordinate_Elements = ["SubordinateId", "RTvalue", "MZratio", "Intensity", "Charge", "Quality"] 

### user params

'''
# Todo without loops
# get labels for first column description
for feature in itertools.islice(features, 0, 1):
  k = []  # start with empty list to fill with key-value pairs
  feature.getKeys(k) # explore available key-value pairs
  for userparam in k:
    feature_labels.append(userparam)
    subordinate_labels.append(userparam)
'''

## export routine to save as csv
## files: feature.csv, subordinate.csv
with open('feature.csv', 'wb') as featurefile:
  featurewriter = csv.writer(featurefile, delimiter="\t", lineterminator='\n')
  #featurefile.write("feature Id \t\t\t\t  RT value \t\t\t\t  MZ ratio \t\t\t\t  Intensity \t\t Charge \t\t Quality \t\t" + '\n')
  #loop across features

  # feature file with parameters
  row_counter = 0
  for feature in features:
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
  subord_userparams_labels = []
  for feature in features:
    subord_userparams_labels = subordinate_Elements
    key_sub = []
    if feature.getSubordinates():
      subordinates = feature.getSubordinates()
      currentrow = []
      for subordinate in subordinates:
        subordinateselect = (subordinate.getUniqueId(), subordinate.getRT(), subordinate.getMZ() , subordinate.getIntensity(), subordinate.getCharge(), subordinate.getOverallQuality())
        currentrow.extend(list(subordinateselect))
        subordinate.getKeys(key_sub)
        for userparam in key_sub:
          subord_userparams_labels.append(userparam)
          currentrow.append(subordinate.getMetaValue(userparam))

      if row_counter == 0:
        row_counter = 1
        subordinatefile.write('\t'.join(subord_userparams_labels) + '\n')
        subordinatewriter.writerow(currentrow)
      else:
        subordinatewriter.writerow(currentrow)



'''
#loop across subordinates
#loop across user params
feature columns + param columns
# subordinates + params
subordinate columns + param columns


## export routine to save into csv
## files: feature.csv, subordinate.csv, feature_params.csv, subordinate_params.csv
## https://stackoverflow.com/questions/4617034/how-can-i-open-multiple-files-using-with-open-in-python
with\
  open('feature.csv', 'wb') as featurefile,\
  open('subordinate.csv', 'wb') as subordinatefile:
  featurewriter = csv.writer(featurefile, delimiter="\t", lineterminator='\n')
  subordinatewriter = csv.writer(subordinatefile, delimiter='\t', lineterminator='\n')

  featurefile.write("feature Id \t\t\t\t  RT value \t\t\t\t  MZ ratio \t\t\t\t  Intensity \t\t Charge \t\t Quality \t\t" + '\n')
  subordinatefile.write("RT value \t\t\t\t  MZ ratio \t\t\t\t  Intensity \t\t Charge \t\t Quality \t\t\t\t subordinate Id " + '\n')

  print(featureElements)
  #for feature in features:
  for feature in itertools.islice(features, 0, 4):
    featureselect = (feature.getUniqueId(), feature.getRT(), feature.getMZ() , feature.getIntensity(), feature.getCharge(), feature.getOverallQuality())  
    featurewriter.writerow(featureselect)
    print('\t'.join(map(str, featureselect)))
    # check for subordinates if true
    if feature.getSubordinates():
      subordinates = feature.getSubordinates()
      print("   Subordinate Id")
      for subordinate in subordinates:
        subordinateselect1 = (subordinate.getUniqueId(), subordinate.getRT(), subordinate.getMZ() , subordinate.getIntensity(), subordinate.getCharge(), subordinate.getOverallQuality())
        subordinateselect2 = (subordinate.getRT(), subordinate.getMZ() , subordinate.getIntensity(), subordinate.getCharge(), subordinate.getOverallQuality(), subordinate.getUniqueId())

        subordinatewriter.writerow(subordinateselect2)
        print("   " + '\t'.join(map(str, subordinateselect1)))


# user parameter files
# fetch feature user params
#for feature in features:
for feature in itertools.islice(features, 0, 6):
  currentcolumn = []   #column with current user param values
  k = []  # start with empty list to fill with key-value pairs
  feature.getKeys(k) # explore available key-value pairs
  currentcolumn.append(feature.getUniqueId())
  for userparam in k:
    currentcolumn.append(feature.getMetaValue(userparam))
  columns.append(currentcolumn)

feature_params  = zip(feature_labels, *columns)
with open('feature_params.csv','wb') as paramfile:
  writer = csv.writer(paramfile, delimiter='\t')  #, lineterminator='\n')
  writer.writerows(feature_params)








## export routine to save into csv
## files: feature.csv, subordinate.csv, feature_params.csv, subordinate_params.csv
## https://stackoverflow.com/questions/4617034/how-can-i-open-multiple-files-using-with-open-in-python
with\
  open('feature.csv', 'wb') as featurefile,\
  open('subordinate.csv', 'wb') as subordinatefile:
  featurewriter = csv.writer(featurefile, delimiter="\t", lineterminator='\n')
  subordinatewriter = csv.writer(subordinatefile, delimiter='\t', lineterminator='\n')

  featurefile.write("feature Id \t\t\t\t  RT value \t\t\t\t  MZ ratio \t\t\t\t  Intensity \t\t Charge \t\t Quality \t\t" + '\n')
  subordinatefile.write("RT value \t\t\t\t  MZ ratio \t\t\t\t  Intensity \t\t Charge \t\t Quality \t\t\t\t subordinate Id " + '\n')

  print(featureElements)
  #for feature in features:
  for feature in itertools.islice(features, 0, 4):
    featureselect = (feature.getUniqueId(), feature.getRT(), feature.getMZ() , feature.getIntensity(), feature.getCharge(), feature.getOverallQuality())  
    featurewriter.writerow(featureselect)
    print('\t'.join(map(str, featureselect)))
    # check for subordinates if true
    if feature.getSubordinates():
      subordinates = feature.getSubordinates()
      print("   Subordinate Id")
      for subordinate in subordinates:
        subordinateselect1 = (subordinate.getUniqueId(), subordinate.getRT(), subordinate.getMZ() , subordinate.getIntensity(), subordinate.getCharge(), subordinate.getOverallQuality())
        subordinateselect2 = (subordinate.getRT(), subordinate.getMZ() , subordinate.getIntensity(), subordinate.getCharge(), subordinate.getOverallQuality(), subordinate.getUniqueId())

        subordinatewriter.writerow(subordinateselect2)
        print("   " + '\t'.join(map(str, subordinateselect1)))


# fetch subordinate user params
#for feature in features:
subordinate_labels.append("Subordinate Id")  #Id, label columns columns with id, rows with labels 
for feature in itertools.islice(features, 0, 1):
  columns = []
  if feature.getSubordinates():
    subordinates = feature.getSubordinates()
    for subordinate in subordinates:
      currentcolumn = []   #column with current user param values
      k = []  # start with empty list to fill with key-value pairs
      subordinate.getKeys(k) # explore available key-value pairs
      currentcolumn.append(subordinate.getUniqueId())
      for userparam in k:
        currentcolumn.append(subordinate.getMetaValue(userparam))
      columns.append(currentcolumn)

print(columns)

subordinate_params = zip(subordinate_labels, *columns)
with open('subordinate_params.csv','wb') as paramfile:
  writer = csv.writer(paramfile, delimiter='\t')  #, lineterminator='\n')
  writer.writerows(subordinate_params)


'''