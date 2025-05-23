import requests 
import pandas as pd 
import json
from datetime import datetime

def run_weather_etl():

    API_key = ''

    countries = ['India','London','Jamaica', 'Haiti', 'Montserrat', 'Barbados', 'Cuba', 'Dominican Republic', 'Saint Lucia', 'Antigua and Barbuda', 'Belize', 'Aruba']

    caribbean_countries = []
    maxtemp = []
    mintemp = []
    humidity = []
    weather = []
    windspeed = []

    for country_names in countries:
        
        url = f'http://api.openweathermap.org/data/2.5/weather?q={country_names}&APPID={API_key}&units=imperial'
        
        response = requests.get(url)
            
        data = response.json()
            
        formatted_json = json.dumps(data, sort_keys = True, indent = 4)

        caribbean_countries.append(data['name'])
        maxtemp.append(data['main']['temp_max'])
        mintemp.append(data['main']['temp_min'])
        humidity.append(data['main']['humidity'])
        weather.append(data['weather'][0]['description'])
        windspeed.append(data['wind']['speed'])
            

    countries_weather_df = pd.DataFrame()
    countries_weather_df['Names'] = caribbean_countries
    countries_weather_df['Max_Temp'] = maxtemp
    countries_weather_df['Min_Temp'] = mintemp
    countries_weather_df['Humidity'] = humidity
    countries_weather_df['Weather'] = weather
    countries_weather_df['WindSpeed'] = windspeed

    countries_weather_df.to_csv('weather.csv')
