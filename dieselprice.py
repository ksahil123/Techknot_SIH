
import requests 
from bs4 import BeautifulSoup

#URL = 'https://www.india.com/petrol-diesel-prices/'


def diesel_price(city):
	headers = {"User-Agent":'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}
	state = ['delhi','mumbai','kolkata','chennai','bengaluru','ahmedabad']
	state = set(state)
	#city = input('Enter state:')
	city = city.lower()
	if city in state:
		newURL = f'https://www.india.com/petrol-diesel-prices/{city}/'
		page = requests.get(newURL, headers=headers)
		soup = BeautifulSoup(page.content,'html.parser')
		table = soup.find('table',attrs={'class': 'todays_oil_status_table'})
		table_row = table.tbody.find_all('tr')
		table_data = table_row[1].find_all('td')
		price = table_data[1].find('span',attrs={'class':'rate arrow-down'}).get_text()
		price = float(price.strip())
	else:
		newURL = f'https://www.india.com/petrol-diesel-prices/mumbai/'
		page = requests.get(newURL, headers=headers)
		soup = BeautifulSoup(page.content,'html.parser')
		table = soup.find('table',attrs={'class': 'todays_oil_status_table'})
		table_row = table.tbody.find_all('tr')
		table_data = table_row[1].find_all('td')
		price = table_data[1].find('span',attrs={'class':'rate arrow-down'}).get_text()
		price = float(price.strip())
	return price





