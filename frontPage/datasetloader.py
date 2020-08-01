import pandas as pd

def getDataset():
	dataset = pd.read_csv('/home/akshatchauhan/Music/SIH2020/VERY_NICE_VERY_CLEAN.csv')
	return dataset