import requests
import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd
import os.path

<<<<<<< HEAD
=======
# Get the absolute path of the directory where the script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the path to the "my_directory" directory relative to the script directory
parent_dir = os.path.dirname(script_dir)
raw_data_path = os.path.join(parent_dir, "raw_data")

>>>>>>> 0f2688881886502959910d4a9d62118203be9ae4
def get_weather(city, years=10, overwrite=False):

    '''
    This function receives the name of a city and a number of years, and returns a dataframe
    with weather data from this city during those past years
    '''
<<<<<<< HEAD

    path = '/home/caiodamasceno/code/Johnny4good/electroprophet/raw_data/df_' + city.lower() + '_weather.csv'
    file_exists = os.path.isfile(path)

    if file_exists and not overwrite:

        print('Found a file for', city + '.','Importing...')

=======
    
    path = raw_data_path + '/df_' + city.lower() + '_weather.csv'
    file_exists = os.path.isfile(path) 
    
    if file_exists and not overwrite:
        
        print('Found a file for', city + '.', 'Importing...')
        
>>>>>>> 0f2688881886502959910d4a9d62118203be9ae4
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
<<<<<<< HEAD
        end_date = (datetime.date.today() - relativedelta(days=8)).strftime('%Y-%m-%d')
        start_date = (datetime.date.today() - relativedelta(years=years)).strftime('%Y-%m-%d')
=======
        end_date = (datetime.date.today() - relativedelta(days=8)).strftime('%Y-%m-%d') 
        #start_date = (datetime.date.today() - relativedelta(years=years)).strftime('%Y-%m-%d')
        start_date = '2013-01-01'
>>>>>>> 0f2688881886502959910d4a9d62118203be9ae4

        # So we make the request to the weather API archive
        weather_response = requests.get('https://archive-api.open-meteo.com/v1/archive',
                           params = {'latitude': lat,
                                    'longitude': lon,
                                    'start_date': start_date,
                                    'end_date': end_date,
                                    'hourly': weather_params,
                                    'timezone': 'auto'}).json()
<<<<<<< HEAD

        weather_df = pd.DataFrame(weather_response['hourly'], columns = ['time'] + weather_params)

        weather_df.to_csv(path, index=False)

    print('Done ✅')
    return weather_df

def get_energy_production(limit, offset, refine):

    # create path or overwrite path --> see function caio for now we just request the data

    #params to pass into the requests
    params = {'limit': limit, 'offset': offset, 'refine': f'libelle_region:{refine}'}

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
    df_final = pd.concat([df_2013_2022, df_2022_today], sort=False,join="inner")

    #transform the column "date_heure", so that it is compatible with the weather data
    df_final.insert(0, "time", df_final['date'] + ' ' + df_final['heure'])
    df_final['time'] =  pd.to_datetime(df_final['time'])
    df_final = df_final.sort_values('time')

    return df_final
=======
        
        weather_df = pd.DataFrame(weather_response['hourly'], columns = ['time'] + weather_params)
        weather_df['time'] = pd.to_datetime(weather_df['time'], format='%Y-%m-%d')
        weather_df = weather_df.set_index('time')
                
        weather_df.to_csv(path)
    
    print('Done ✅')
    return weather_df

def get_energy_production(limit, offset, refine,overwrite=False):
    
    '''
    This function receives the name of a region, a limit and an offset, and returns a dataframe 
    with energy production data from this region
    '''

    path = raw_data_path + '/df_' + refine.lower().replace(" ", "_") + '_energy_production.csv'
    file_exists = os.path.isfile(path)
    
    if file_exists and not overwrite:
        
        print('Found a file for',refine + '.', 'Importing...')
        
        energy_production_df = pd.read_csv(path, index_col=0, low_memory=False)
    
    else:
        
        print('Creating a new .csv file for', refine)

        #params to pass into the requests
        params = {'limit': limit, 'offset': offset, 'refine': f'libelle_region:{refine}'}

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
        
        energy_production_df.to_csv(path)
        
    print('Done ✅')
    return energy_production_df

def merge_weather_energy_df(city, refine, target, years=10, limit=-1, offset=0, overwrite=False):
    # get weather data
    weather_df = get_weather(city, years, overwrite)

    # get energy production data and target
    energy_df = get_energy_production(limit, offset, refine)
    energy_target = energy_df[["time", target]]

    # merge the two dataframes on the 'time' column only on full hours and drop the rest
    merged_df = pd.merge(weather_df, energy_target, on='time', how= "left")
    merged_df = merged_df.set_index('time', inplace=True)

    return merged_df
>>>>>>> 0f2688881886502959910d4a9d62118203be9ae4
