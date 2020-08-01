import numpy as np
import pandas as pd
import json

def searchStart(src, dest):
	with open("/dataset/dictionary.json") as x:
		stationDict = json.load(x)

	return stationDict[src][dest]

def searchEnd(df, src, dest, i):
	while i <= 1769419 and df.loc[i,'FROM_STN'] == src and df.loc[i,'TO_STN'] == dest:
		i = i+1
	return i

def datasetLoader():
	dataset = pd.read_csv("VERY_NICE_VERY_CLEAN.csv")
	return dataset

# This method will give the required slice of dataset
def getSlice(df, src, dest):
	iStart = searchStart(src, dest)
	iEnd = searchEnd(df, src, dest, iStart)
	return df.loc[iStart:iEnd-1, :]

"""
def decoder(src, dest):
	data = pd.read_excel("")
	print(data)
    sorted_by_city = data.sort_values(['CITY'], ascending=True)
	
	src_code_df = sorted_by_city['CITY'] == 'src'
    print(src_code_df)
	s = src_code['STATE']

	dest_code = sorted_by_city['CITY'] == 'dest'
	d = dest_code['STATE']

	return s,d
"""
def modelCreator():
	fg = multiplelinear()
	return prediction

