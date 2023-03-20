from prophecy.get_data_forecast import WeatherForecast
from prophecy.process_forecast_data import ForecastDataframe
from prophecy.get_data import WeatherEnergy
import tensorflow as tf
import sys
import pandas as pd
import numpy as np
import warnings
from statsmodels.tsa.seasonal import seasonal_decompose
import os
# Test

sys.path.append('../')
def get_average(df, target):

    tsm_decompose = seasonal_decompose(np.array(df[target]), model = 'additive', period = 24)
    df['observed'] = tsm_decompose.observed
    observed = df['observed'].dropna().mean()

    return observed

def main(city):

    # Filter out RuntimeWarning
    warnings.filterwarnings("ignore", category=RuntimeWarning)

    # Getting the forecast data
    wind_df = ForecastDataframe('Heudicourt').return_scaled_forecast()
    sun_df = ForecastDataframe('Cestas').return_scaled_forecast()
    cons_df = ForecastDataframe(city).return_scaled_forecast()

    # Loading the models
    wind_model = tf.keras.models.load_model('/home/jonathand/code/Johnny4good/electroprophet/saved_model/wind_model')
    sun_model = tf.keras.models.load_model('/home/jonathand/code/Johnny4good/electroprophet/saved_model/sun_model')
    cons_model = tf.keras.models.load_model('/home/jonathand/code/Johnny4good/electroprophet/saved_model/cons_model')

    # Loading the historical data
    wind_old_df = pd.read_csv('/home/jonathand/code/Johnny4good/electroprophet/raw_data/wind_old.csv', on_bad_lines='skip', index_col = 0)
    sun_old_df = pd.read_csv('/home/jonathand/code/Johnny4good/electroprophet/raw_data/sun_old.csv', on_bad_lines='skip', index_col = 0)
    cons_old_df = pd.read_csv('/home/jonathand/code/Johnny4good/electroprophet/raw_data/cons_old.csv', on_bad_lines='skip', index_col = 0)

    # Defining the params
    targets = {'eolien': ('Hauts-de-France','eolien',['Heudicourt','Bucy-les-Pierrepont','Riencourt'],wind_df,wind_model,wind_old_df),
       'solaire':('Nouvelle-Aquitaine','solaire',['Cestas'],sun_df,sun_model,sun_old_df),
        'consommation': ('Hauts-de-France','consommation',[city],cons_df,cons_model,cons_old_df)}

    forecasts = []
    averages = []
    old_energy = []

    # Looping over the 3 models
    for key in targets:
        processed_df = targets[key][5]
        old_energy_df = processed_df[[key]]
        old_df = processed_df.drop(columns=key)

        new_df = targets[key][3]

        input_data = np.array(pd.concat([old_df, new_df], axis=0))

        # Define the desired number of hours in the output
        num_hours = 24

        # Compute the number of timesteps in each hour
        timesteps_per_hour = input_data.shape[0] // num_hours

        # Reshape the original data into the desired shape
        hourly_data = np.reshape(input_data[:timesteps_per_hour*num_hours], (num_hours, timesteps_per_hour, -1))

        # Make a prediction for the next 24 hours
        forecast = targets[key][4].predict(hourly_data, verbose=0)
        forecast[forecast < 0] = 0

        forecasts.append(forecast)
        old_energy.append(old_energy_df)

        forecast_df = pd.DataFrame(forecast, index = new_df.index, columns = [key])

        # Getting the averages
        avg = get_average(pd.concat([old_energy_df, forecast_df], axis=0), key)

        averages.append(avg)
        print(avg)

    #recomendations = ((forecasts[0]+forecasts[1])/np.mean(forecasts[0]+forecasts[1]))/(forecasts[2]/np.mean(forecasts[2]))>1
    production_dev = ((forecasts[0]+forecasts[1]) - (averages[0]+averages[1])) / (averages[0]+averages[1])
    consumption_dev = (forecasts[2] - averages[2]) / averages[2]
    recomendations = production_dev - consumption_dev

    recomendations_list = []

    for rec in recomendations:

        if rec > 0.2:
            recomendations_list.append('Good')
        elif rec < -0.2:
            recomendations_list.append('Bad')
        else:
            recomendations_list.append('Normal')

    # Reset the warning filters to the default settings
    warnings.filterwarnings("default", category=RuntimeWarning)

    return recomendations_list
