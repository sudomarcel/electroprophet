import pandas as pd
import requests
from datetime import date
<<<<<<< HEAD
from dateutil.relativedelta import relativedelta
from geopy.geocoders import Nominatim

#
# See the notebook "notebooks/Jonathan_notebook_weatherforecast.ipynb"
#

class WeatherForecast:
    def __init__(self, city:str, days:int):
        self.city = city
        self.days = days
=======
from geopy.geocoders import Nominatim
from datetime import datetime,timedelta


#rewrite to accept list (if we need to improve)

class WeatherForecast:
    def __init__(self, city:str):
        self.city = city
>>>>>>> 0bb7176f6d9a1edfcee989587e267277be7d05c9

    def get_city_lonlan(self):
        '''
        This function receives the name of one city and returns the lat and lon of that city
        in a dictionary
        '''

        # Create a geolocator object
        geolocator = Nominatim(user_agent="my_app")

        #save the coordinates of each city in self.city in a dictionary
        coordinates = {}

        # Get the location of the city
        location = geolocator.geocode(self.city)

        #check if the location exists
        if location:
            lat, lon = location.latitude, location.longitude # Extract the latitude and longitude
            coordinates[self.city] = [lat,lon]
        else:
            print(f"Could not retrieve coordinates for {self.city}")

        return coordinates

    def get_weather_forecast(self):

        '''
        This function receives
            * the name of the city list
            * a number of days of weather forecast we want to work on

        This function returns a dataframe with the average of the weather data from these city list during those days of forecast
        '''

        # First we declare the weather parameters. Here we'll be taking all params supported by the API
        weather_params = ['temperature_2m','relativehumidity_2m','dewpoint_2m',
                      'apparent_temperature','pressure_msl','surface_pressure',
                      'precipitation','rain','snowfall','cloudcover',
                      'cloudcover_low','cloudcover_mid','cloudcover_high',
                      'shortwave_radiation','direct_radiation','direct_normal_irradiance',
                      'diffuse_radiation','windspeed_10m','windspeed_120m',
                      'winddirection_10m','winddirection_120m','windgusts_10m',
<<<<<<< HEAD
                      'et0_fao_evapotranspiration','vapor_pressure_deficit',
                      'soil_temperature_0cm','soil_temperature_6cm',
                      'soil_temperature_18cm','soil_temperature_54cm',
                      'soil_moisture_0_1cm','soil_moisture_1_3cm',
                      'soil_moisture_3_9cm','soil_moisture_9_27cm', 'soil_moisture_27_81cm']

        # Then we compute the dates used to get the weather forecast data

        # end_date : today + number of days of forecast (self.days)
        end_date = (date.today() + relativedelta(days=self.days)).strftime('%Y-%m-%d')

        #start_date : today at midnight
        start_date = (date.today()).strftime('%Y-%m-%d')
=======
                      'et0_fao_evapotranspiration','weathercode','vapor_pressure_deficit',
                      'soil_temperature_0cm','soil_temperature_6cm',
                      'soil_temperature_18cm','soil_temperature_54cm',
                      'soil_moisture_0_1cm','soil_moisture_3_9cm','soil_moisture_9_27cm',
                      'soil_moisture_27_81cm']

        # Then we compute the dates used to get the weather forecast data

>>>>>>> 0bb7176f6d9a1edfcee989587e267277be7d05c9

        #call the method to receive the coordinates from the self.city list
        coordinates = self.get_city_lonlan()

<<<<<<< HEAD
        #create an empty dataframe
        # cities = []

=======
>>>>>>> 0bb7176f6d9a1edfcee989587e267277be7d05c9
        #create a dataframe with weather params for the selected city and store it
        lat = coordinates[self.city][0]
        lan = coordinates[self.city][1]


        # So we make the request to the weather API archive
        weather_forecast_response= requests.get('https://api.open-meteo.com/v1/forecast',
                            params = {'latitude': lat,
                                        'longitude': lan,
<<<<<<< HEAD
                                        'forecast_days' : self.days,
=======
                                        'forecast_days' : 2,
>>>>>>> 0bb7176f6d9a1edfcee989587e267277be7d05c9
                                        'hourly': weather_params,
                                        'timezone': 'auto'}).json()

        weather_forecast_df = pd.DataFrame(weather_forecast_response['hourly'], columns = ['time'] + weather_params)
        weather_forecast_df['time'] = pd.to_datetime(weather_forecast_df['time'], format='%Y-%m-%d')
<<<<<<< HEAD
        weather_forecast_df = weather_forecast_df.set_index('time')

=======
        #get the start and end time
        start_time = datetime.now()
        end_time = start_time + timedelta(hours=24)
        weather_forecast_df = weather_forecast_df[(weather_forecast_df['time'] >= start_time) & (weather_forecast_df['time'] < end_time)]
        #set time as index
        weather_forecast_df = weather_forecast_df.set_index('time')
>>>>>>> 0bb7176f6d9a1edfcee989587e267277be7d05c9
        # Format float to 1 decimal, sum the 3 tables and return the average
        pd.options.display.float_format = "{:,.1f}".format


        return weather_forecast_df

    def rename_columns(self):
        weather_df_old_columns_names = self.get_weather_forecast()

<<<<<<< HEAD
        weather_params_history_data = ["time",'temperature_2m','relativehumidity_2m','dewpoint_2m',
=======
        weather_params_history_data = ['temperature_2m','relativehumidity_2m','dewpoint_2m',
>>>>>>> 0bb7176f6d9a1edfcee989587e267277be7d05c9
                      'apparent_temperature','pressure_msl','surface_pressure',
                      'precipitation','rain','snowfall','cloudcover',
                      'cloudcover_low','cloudcover_mid','cloudcover_high',
                      'shortwave_radiation','direct_radiation','direct_normal_irradiance',
                      'diffuse_radiation','windspeed_10m','windspeed_100m',
                      'winddirection_10m','winddirection_100m','windgusts_10m',
<<<<<<< HEAD
                      'et0_fao_evapotranspiration','vapor_pressure_deficit',
=======
                      'et0_fao_evapotranspiration','weathercode','vapor_pressure_deficit',
>>>>>>> 0bb7176f6d9a1edfcee989587e267277be7d05c9
                      'soil_temperature_0_to_7cm','soil_temperature_7_to_28cm',
                      'soil_temperature_28_to_100cm','soil_temperature_100_to_255cm',
                      'soil_moisture_0_to_7cm','soil_moisture_7_to_28cm',
                      'soil_moisture_28_to_100cm','soil_moisture_100_to_255cm']

        weather_df_old_columns_names.columns = weather_params_history_data
        return weather_df_old_columns_names
