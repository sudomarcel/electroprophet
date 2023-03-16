import pandas as pd
import requests
from datetime import datetime, date
from dateutil.relativedelta import relativedelta

class WeatherEnergy:
    def __init__(self, limit, offset, refine, city, target, years=10):
        self.city = city
        self.years = years
        self.limit = limit
        self.offset = offset
        self.refine = refine
        self.target = target

    def get_weather(self):

        '''
        This function receives the name of a city and a number of years, and returns a dataframe
        with weather data from this city during those past years
        '''

        # First we declare the weather parameters. Here we'll be taking all params supported by the API
        weather_params = ['temperature_2m','relativehumidity_2m','dewpoint_2m',
                      'apparent_temperature','pressure_msl','surface_pressure',
                      'precipitation','rain','snowfall','cloudcover',
                      'cloudcover_low','cloudcover_mid','cloudcover_high',
                      'shortwave_radiation','direct_radiation','direct_normal_irradiance',
                      'diffuse_radiation','windspeed_10m','windspeed_100m',
                      'winddirection_10m','winddirection_100m','windgusts_10m',
                      'et0_fao_evapotranspiration','weathercode','vapor_pressure_deficit',
                      'soil_temperature_0_to_7cm','soil_temperature_7_to_28cm',
                      'soil_temperature_28_to_100cm','soil_temperature_100_to_255cm',
                      'soil_moisture_0_to_7cm','soil_moisture_7_to_28cm',
                      'soil_moisture_28_to_100cm','soil_moisture_100_to_255cm']

        # This request is done in order to get the latitude and longitude of the desired city
        city_response = requests.get('https://geocoding-api.open-meteo.com/v1/search',
                           params = {'name': self.city}).json()

        lat = city_response['results'][0]['latitude']
        lon = city_response['results'][0]['longitude']

        # Then we compute the dates used to get the weather data
        ## The API only has data until 9 days ago
        end_date = (date.today() - relativedelta(days=8)).strftime('%Y-%m-%d')

        #start_date = (datetime.date.today() - relativedelta(years=years)).strftime('%Y-%m-%d')
        start_date = (date.today() - relativedelta(years=self.years)).strftime('%Y-%m-%d')

        # So we make the request to the weather API archive
        weather_response = requests.get('https://archive-api.open-meteo.com/v1/archive',
                           params = {'latitude': lat,
                                    'longitude': lon,
                                    'start_date': start_date,
                                    'end_date': end_date,
                                    'hourly': weather_params,
                                    'timezone': 'auto'}).json()

        weather_df = pd.DataFrame(weather_response['hourly'], columns = ['time'] + weather_params)
        weather_df['time'] = pd.to_datetime(weather_df['time'], format='%Y-%m-%d')
        weather_df = weather_df.set_index('time')

        return weather_df

    def get_energy_production(self):

        '''
        This function receives the name of a region, a limit and an offset, and returns a dataframe
        with energy production data from this region
        '''

        #params to pass into the requests
        params = {'limit': self.limit, 'offset': self.offset, 'refine': f'libelle_region:{self.refine}'}

        #request the API for the data from 2013-2022
        url_2013_2022 = 'https://odre.opendatasoft.com/api/v2/catalog/datasets/eco2mix-regional-cons-def/exports/json'
        response_2013_2022 = requests.get(url=url_2013_2022,params = params).json()

        #transform API request into a dataframe
        df_2013_2022 = pd.DataFrame(response_2013_2022)

        #request the API for the data from 2022-today
        url_2022_today = 'https://odre.opendatasoft.com/api/v2/catalog/datasets/eco2mix-regional-tr/exports/json'
        response_2022_today = requests.get(url=url_2022_today,params = params).json()

        #transform API request into a dataframe
        df_2022_today = pd.DataFrame(response_2022_today)

        #merge those two together on just columns that exist in the first one
        energy_production_df = pd.concat([df_2013_2022, df_2022_today], sort=False,join="inner")

        #transform the column "date_heure", so that it is compatible with the weather data
        energy_production_df.insert(0, "time", energy_production_df['date'] + ' ' + energy_production_df['heure'])
        energy_production_df['time'] =  pd.to_datetime(energy_production_df['time'])
        energy_production_df = energy_production_df.sort_values('time')
        energy_production_df = energy_production_df.set_index('time')

        return energy_production_df

    def merge(self):

        '''
        This function takes in the get_weather and the get_energy_production dataframes
        and merges them into a merged_df dataframe
        '''

        #calls the get_weather function and stores the result in a dataframe
        weather_df = self.get_weather()

        #calls the get_energy_production and stores the result in a dataframe
        energy_production_df = self.get_energy_production()

        #merges the two dataframes and returns the merged_df
        merged_df = pd.merge(weather_df, energy_production_df[self.target], left_index=True, right_index=True)

        return merged_df
