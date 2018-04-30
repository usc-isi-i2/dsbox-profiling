#!/usr/bin/env python3

from d3m import container
from d3m.metadata.base import DataMetadata, ALL_ELEMENTS

from os import path
from dsbox.datapreprocessing.profiler import Profiler, Hyperparams
import pandas as pd
import json

# Example for the documentation of the TA1 pipeline submission process
#
# It executes a TA1 pipeline using a ta1-pipeline-config.json file that follows this structure:
#  {
#    "train_data":"path/to/train/data/folder/",
#    "test_data":"path/to/test/data/folder/",
#    "output_folder":"path/to/output/folder/"
#  }

# Load the json configuration file
with open("ta1-pipeline-config.json", 'r') as inputFile:
    jsonCall = json.load(inputFile)
    inputFile.close()

# Load the problem description schema
with open( path.join(jsonCall['train_data'], 'problem_TRAIN', 'problemDoc.json' ) , 'r') as inputFile:
    problemSchema = json.load(inputFile)
    inputFile.close()

# Load the json dataset description file
with open( path.join(jsonCall['train_data'], 'dataset_TRAIN', 'datasetDoc.json' ) , 'r') as inputFile:
    datasetSchema = json.load(inputFile)
    inputFile.close()

# Load dataset
ds_uri = 'file://' + path.join(jsonCall['train_data'], 'dataset_TRAIN', 'datasetDoc.json')
ds = container.Dataset(resources=dict(), metadata=DataMetadata())
ds = ds.load(ds_uri)

# Profile dataset
param = Hyperparams.sample()
prof = Profiler(hyperparams=param)
ds2 = prof.produce(inputs=ds)

# Get resource Ids, return ['0'] for this dataset
print(ds.metadata.get_elements( () ))

# Get available columns, returns [0, 1, 2, ..., 30] for 38_sick dataset
print(ds.metadata.get_elements(('0', ALL_ELEMENTS)))

# Metadata for column 1
column_one_metadata = ds.metadata.query(('0', ALL_ELEMENTS, 1))

# Print metadata for entire dataset as json
ds2.metadata.pretty_print()


###### The rest of this file has nothing to do with the DSBox data profiling primitive.
###### Needed just to pass the pipeline submission

# Get the target and attribute column ids from the dataset schema for training data
trainAttributesColumnIds = [ item['colIndex'] for item in datasetSchema['dataResources'][0]['columns'] if 'attribute' in item['role'] ]
trainTargetsColumnIds = [ item['colIndex'] for item in problemSchema['inputs']['data'][0]['targets'] ]

# Exit if more than one target
if len(trainTargetsColumnIds) > 1:
    print('More than one target in the problem. Exiting.')
    exit(1)

# Get the attribute column ids from the problem schema for test data (in this example, they are the same)
testAttributesColumnIds = trainAttributesColumnIds

# Load the tabular data file for training, replace missing values, and split it in train data and targets
trainDataResourcesPath = path.join(jsonCall['train_data'], 'dataset_TRAIN', datasetSchema['dataResources'][0]['resPath'])
trainData = pd.read_csv( trainDataResourcesPath, header=0, usecols=trainAttributesColumnIds).fillna('0').replace('', '0')
trainTargets = pd.read_csv( trainDataResourcesPath, header=0, usecols=trainTargetsColumnIds).fillna('0').replace('', '0')

# Load the tabular data file for training, replace missing values, and split it in train data and targets
testDataResourcesPath = path.join(jsonCall['test_data'], 'dataset_TEST', datasetSchema['dataResources'][0]['resPath'])
testData = pd.read_csv( testDataResourcesPath, header=0, usecols=testAttributesColumnIds).fillna('0').replace('', '0')

# Get the d3mIndex of the testData
d3mIndex = pd.read_csv( testDataResourcesPath, header=0, usecols=['d3mIndex'])
target_name = problemSchema['inputs']['data'][0]['targets'][0]['colName']

# To create a dummy prediction
random_sample = trainTargets[target_name].dropna()[0]
testData[target_name] = random_sample
predictedTargets = testData[target_name]

# Get the file path of the expected outputs
outputFilePath = path.join(jsonCall['output_folder'], problemSchema['expectedOutputs']['predictionsFile'])

# Outputs the predicted targets in the location specified in the JSON configuration file
with open(outputFilePath, 'w') as outputFile:
    output = predictedTargets.to_csv(outputFile, header=True, index=True, index_label='d3m')
