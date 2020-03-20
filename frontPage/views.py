from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import *
import urllib.request
import json
import pyqrcode
import requests
from geopy.geocoders import Nominatim
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




# Create your views here.
def firstPage(request):
	return render(request,'frontPage/index.html',{'title':'Tezy-Home'})

def aboutPage(request):
	return render(request,'frontPage/about.html',{'title':'Tezy-About'})

def setAddressPage(request):
	if request.method == "POST":
		completeForm = addressForm(request.POST)
		if completeForm.is_valid():
			# get origin and destination from the form
			origin = completeForm.cleaned_data['origin'].replace(' ','+')
			destination = completeForm.cleaned_data['destination'].replace(' ','+')

			try:
				# calculating coordinates of the origin and destination
				geolocator = Nominatim(user_agent='tezy')
				origin_loc = geolocator.geocode(origin)
				dest_loc = geolocator.geocode(destination)
				print(origin_loc.latitude,origin_loc.longitude)
				print(dest_loc.latitude,dest_loc.longitude)
				org_string = str(origin_loc.latitude)+"%2C"+str(origin_loc.longitude)+"%3B"
				dest_string = str(dest_loc.latitude)+"%2C"+str(dest_loc.longitude)+"%3B"
			except:
				print('Error occurred in fetching latitude and longitude')
				return render(request,'frontPage/directions.html',{'err':'Error fetching coordinates'},{'title':'Tezy-Navigation'})

			try:
				# using coordinates to calculate distance and travel time
				url = "https://trueway-matrix.p.rapidapi.com/CalculateDrivingMatrix"

				querystring = {"destinations":dest_string,"origins":org_string}

				headers = {'x-rapidapi-host': "trueway-matrix.p.rapidapi.com",'x-rapidapi-key': "51e28f2319msh1402c97f967f494p14ff9fjsn2453b6f2f065"}

				response = requests.request("GET", url, headers=headers, params=querystring)

				details = json.loads(response.text)
				print(details)
				temp_list = details.get('distances')
				distance = temp_list[0][0]
				distance = distance/1000
				distance = round(distance,1)
				print(distance)
				temp_list = details.get('durations')

				time = temp_list[0][0]
				print(time)
				time = time/3600
				print(time)
				time = round(time,1)
				print(time)
			except:
				print('Error occurred in fetching distance and duration.')
				return render(request,'frontPage/directions.html',{'err':'Error fetching distance and duration'},{'title':'Tezy-Navigation'})

			try:
				# creating qr link to google maps
				endpoint = 'https://www.google.com/maps/dir/?api=1&'
				navigation_request = 'origin={}&destination={}&travelmode=driving'.format(origin,destination)
				map_req = endpoint+navigation_request
				dir_link = pyqrcode.create(map_req)
				dir_link.png("/home/akshatchauhan/noobengine/static/dir.png",scale=5)
			except:
				print('Error occurred in creating Google Map Link.')
				return render(request,'frontPage/directions.html',{'err':'Error creating QR code'},{'title':'Tezy-Navigation'})

			return render(request,'frontPage/directions.html',{'d':distance,'t':time},{'title':'Tezy-Navigation'})

	else:
		addForm = addressForm()
	return render(request,'frontPage/locations.html',{'form':addForm},{'title':'Tezy-Set Address'})

