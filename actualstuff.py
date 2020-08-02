import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder,MultiLabelBinarizer
from sklearn.neural_network import MLPClassifier 
import json
from .import dieselprice as dp

# URL = 'https://www.india.com/petrol-diesel-prices/'
headers = {"User-Agent":'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}


def parseCity(city):
	temp = city.split(' ')
	return str(temp[-1])


def searchStart(src, dest):
	with open("C:/Users/sahil khandelwal/Desktop/SIH/Techknot_SIH-master/Techknot_SIH-master/frontPage/dictionary.json") as x:
		stationDict = json.load(x)

	return int(stationDict[src][dest])

def searchEnd(df, src, dest, i):
	while i <= 1769419 and df.loc[i,'FROM_STN'] == src and df.loc[i,'TO_STN'] == dest:
		i = i+1
	return i

def datasetLoader():
	dataset = pd.read_csv("C:/Users/sahil khandelwal/Desktop/SIH/Techknot_SIH-master/Techknot_SIH-master/frontPage/VERY_NICE_VERY_CLEAN1.csv")
	dataset.drop(dataset.columns[0],axis=1,inplace=True)
	return dataset

# This method will give the required slice of dataset
def getSlice(df, iStart, iEnd):
	return df.loc[iStart:iEnd-1]

def getDiesel(city):

	diesel = dp.diesel_price(city)
	return diesel

def parseDate(date):
	temp = ""
	temp = temp + str(date.month)
	temp = temp + str(date.year)
	return temp
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

def modelCreator(dataset, dateString, src, dest, diesel, ef):
	
	iStart = searchStart(src, dest)
	iEnd = searchEnd(dataset, src, dest, iStart)	

	# Label Encoding
	le = LabelEncoder()	
	dataset['FROM_STN_temp'] = le.fit_transform(dataset['FROM_STN'])
	dataset['TO_STN_temp'] = le.fit_transform(dataset['TO_STN'])

	# Encoding users input
	src = le.transform([src])
	dest = le.transform([dest])


	# getting the slice
	df = dataset.loc[iStart:iEnd-1]

#	kms = df.loc[0,'KMS_5']
	
	X = df.loc[:,['MONTH_YEAR','FROM_STN_temp','TO_STN_temp','DIESEL','EF']].values
	Y = df.loc[:,['CARD_RATE']].values

	print("SRC: ",src[0])
	print("DEST: ",dest[0])
	#print(Y)
	#print(X)
	mlb = MultiLabelBinarizer()
	Y_enc = mlb.fit_transform(Y)
	dateString = int(dateString)
	ann = MLPClassifier(n_iter_no_change=100)
	ann.fit(X, Y_enc)
	x_test = [[dateString, src[0], dest[0], diesel, ef]]

	y_pred = ann.predict(x_test)

	y_pred = mlb.inverse_transform(y_pred)
	print(y_pred)

	y_pred = y_pred[0]
	print(y_pred)
	if is_empty(y_pred):
		return df.loc[0,"CARD_RATE"]

	return y_pred[-1]