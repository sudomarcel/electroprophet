def get_weather(city, years=10, overwrite=False):
    
    '''
    This function receives the name of a city and a number of years, and returns a dataframe 
    with weather data from this city during those past years
    '''
    
    import requests
    import datetime
    from dateutil.relativedelta import relativedelta
    import pandas as pd
    import os.path
    
    path = '/home/caiodamasceno/code/Johnny4good/electroprophet/raw_data/df_' + city.lower() + '_weather.csv'
    file_exists = os.path.isfile(path) 
    
    if file_exists and not overwrite:
        
        print('Found a file for', city + '.','Importing...')
        
        weather_df = pd.read_csv(path, index_col=0)
        
    else:
        
        print('Creating a new .csv file for', city)
        
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
                           params = {'name': city}).json()

        lat = city_response['results'][0]['latitude']
        lon = city_response['results'][0]['longitude']

        # Then we compute the dates used to get the weather data
        ## The API only has data until 9 days ago
        end_date = (datetime.date.today() - relativedelta(days=8)).strftime('%Y-%m-%d') 
        start_date = (datetime.date.today() - relativedelta(years=years)).strftime('%Y-%m-%d')

        # So we make the request to the weather API archive
        weather_response = requests.get('https://archive-api.open-meteo.com/v1/archive',
                           params = {'latitude': lat,
                                    'longitude': lon,
                                    'start_date': start_date,
                                    'end_date': end_date,
                                    'hourly': weather_params,
                                    'timezone': 'auto'}).json()

        weather_df = pd.DataFrame(weather_response['hourly'], columns = ['time'] + weather_params)
        
        weather_df.to_csv(path, index=False)
    
    print('Done ✅')
    return weather_df
