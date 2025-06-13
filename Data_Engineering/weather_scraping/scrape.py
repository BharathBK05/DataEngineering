import requests
from bs4 import BeautifulSoup
import pandas as pd
import json


with open('E:\\Git\\Python_L1&L2\\Project\\weather_scraping\\cities.json','r') as f:
    data = json.load(f)
cities = data['cities']


base_url = 'https://www.timeanddate.com/weather/india/'

weather_data = []

for city in cities:
    url = base_url + city

    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        #Extracting Temp
        temp = soup.find('div', class_='h2').text.strip()
        temp = temp[0:2] + '°C'

        #Extract the condition
        qlook_div = soup.find('div',id='qlook')
        condition = qlook_div.find_all('p')[0].text.strip()
        feels = qlook_div.find_all('p')[1].text.strip()
        feels = feels.split('°C')
        feels = [i.split(':')[1].strip() for i in feels]

        weather_dic = {'City':city.title(), 'Temperature':temp, 'Condition':condition , 'Feels Like':feels[0], 'Forecast':feels[1],
                       'Wind':feels[2]}
        weather_data.append(weather_dic)
        print('Extracted for city - ',city)
    else:
        print('Failed to fetch data for city - ', city)


#save data to csv
df = pd.DataFrame(weather_data)
df.to_csv('Weather_data.csv',index=False)
print('Done')