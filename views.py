from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import *
import urllib.request
import json
#import pyqrcode
import requests
#from geopy.geocoders import Nominatim
from .import actualstuff as ast
import pandas as pd
#https://www.google.com/maps/dir/?api=1&origin=Space+Needle+Seattle+WA&destination=Pike+Place+Market+Seattle+WA&travelmode=bicycling
"""
import requests

url = "https://trueway-matrix.p.rapidapi.com/CalculateDrivingMatrix"

querystring = {"destinations":"40.629041%2C-74.025606%3B40.630099%2C-73.993521%3B40.644895%2C-74.013818%3B40.627177%2C-73.980853","origins":"40.629041%2C-74.025606%3B40.630099%2C-73.993521%3B40.644895%2C-74.013818%3B40.627177%2C-73.980853"}

headers = {
    'x-rapidapi-host': "trueway-matrix.p.rapidapi.com",
    'x-rapidapi-key': "51e28f2319msh1402c97f967f494p14ff9fjsn2453b6f2f065"
    }

response = requests.request("GET", url, headers=headers, params=querystring)
"""


#dataset = pd.DataFrame()
dataset = ast.datasetLoader()
# Create your views here.
def firstPage(request):
	#dataset = ast.datasetLoader()
	print(dataset.head())

	return render(request,'frontPage/index.html',{'title':'Tezy-Home'})

def aboutPage(request):
	return render(request,'frontPage/about.html',{'title':'Tezy-About'})

def setAddressPage(request):
	if request.method == "POST":
		completeForm = addressForm(request.POST)
		if completeForm.is_valid():
			# get origin destination date weight from the form
			#x,y = decoder(completeForm.origin, completeForm.destination)

			# getting the slice
			
			src = completeForm.cleaned_data['origin'].replace(' ','+')
			#city=ast.getCityName(src)
			#print(src,city)
			dest= completeForm.cleaned_data['destination'].replace(' ','+')
			print(dest)
			#src=ast.parseCity(src)
			#dest=ast.parseCity(dest)
			print(src,dest)	
			date= completeForm.cleaned_data['date']
			print(date)
			weight= completeForm.cleaned_data['weight']
			print(weight)
			dateString = ast.parseDate(date)
			print(dateString)
			diesel=ast.getDiesel(src)
			print(diesel)
			EF=1.5
			# getting the slice
			print(dataset.head())
			rate = ast.modelCreator(dataset, dateString, src, dest, diesel, EF)
			weight = weight*rate
			return render(request,'frontPage/directions.html',{'title':'Tezy-Navigation','d':rate,'t':weight})

	addForm = addressForm()
	print(dataset.head())
	return render(request,'frontPage/locations.html',{'title':'Tezy-Set Address', 'form':addForm})
"""			if df.empty:
				temp = "NO PATH EXISTS FROM SPECIFIED SOURCE TO DESTINATION!"
				return render(request,'frontPage/directions.html',{'title':'Tezy-Navigation','d':temp,'t':0}) 
"""

	


