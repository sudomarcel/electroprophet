from sklearn.compose import make_column_transformer
from sklearn.preprocessing import StandardScaler, RobustScaler, PowerTransformer
import pandas as pd
import numpy as np

class FeaturePreprocessing:
    def __init__(self,df,target=None):
        self.df = df
        self.target = target
        if target!=None:
            self.target = df[target]

    def get_wind_components(self):


        # Convert degrees to radians and store the values into wd_rad
        #wind direction 10 m
        wd_rad_10 = self.df.pop('winddirection_10m')*np.pi / 180

        #wind direction 100 m
        wd_rad_100 = self.df.pop('winddirection_100m')*np.pi / 180

        # Calculate the wind x and y components and store then in two new columns
        # `Wx` and `Wy`
        #wind speed 10 m
        wv_10 = self.df.pop('windspeed_10m')
        self.df['Wx_10'] = wv_10*np.cos(wd_rad_10)
        self.df['Wy_10'] = wv_10*np.sin(wd_rad_10)

        #wind speed 100 m
        wv_100 = self.df.pop('windspeed_100m')
        self.df['Wx_100'] = wv_100*np.cos(wd_rad_100)
        self.df['Wy_100'] = wv_100*np.sin(wd_rad_100)

        return self.df

    def feature_processing(self):
        #has to acces the get_wind_components so change
        #columns to use

        unprocessed_dataframe = self.get_wind_components()
        columns_for_standardscaler = ['temperature_2m','dewpoint_2m',
                                    'apparent_temperature','pressure_msl','surface_pressure',
                                    'Wx_10','Wx_100','Wy_10',
                                    'Wy_100','windgusts_10m','soil_temperature_0_to_7cm',
                                    'soil_temperature_7_to_28cm','soil_temperature_28_to_100cm',
                                    'soil_temperature_100_to_255cm','soil_moisture_0_to_7cm',
                                    'soil_moisture_7_to_28cm','soil_moisture_28_to_100cm',
                                    'soil_moisture_100_to_255cm']

        columns_for_robustscaler = ['cloudcover','cloudcover_low',
                                    'cloudcover_mid','cloudcover_high']

        columns_for_powertransformer = ['relativehumidity_2m','precipitation','rain',
                                        'snowfall', 'shortwave_radiation','direct_radiation',
                                        'direct_normal_irradiance','diffuse_radiation',
                                        'et0_fao_evapotranspiration','vapor_pressure_deficit']

        #function doesnt work like this
        scaler = make_column_transformer(
            (StandardScaler(),columns_for_standardscaler),
            (RobustScaler(),columns_for_robustscaler),
            (PowerTransformer(),columns_for_powertransformer))

        scaled_data = scaler.fit_transform(unprocessed_dataframe)
        scaled_dataframe = pd.DataFrame(scaled_data, columns=scaler.get_feature_names_out())
        processed_dataframe = scaled_dataframe.set_index(unprocessed_dataframe.index)
        return processed_dataframe

    def get_season(self):
        """
        Calls a function data gets the day from the time column,
        outputs whether the day is in the Spring, Summer, Fall or
        Winter and creates
        """
        processed_dataframe = self.feature_processing()
        season = []

        # get the current day of the year
        doy = processed_dataframe.iloc[0].name.timetuple().tm_yday

        # "day of year" ranges for the northern hemisphere
        spring = range(80, 172)
        summer = range(172, 264)
        fall = range(264, 355)
        # winter = everything else

        for doy in range(len(processed_dataframe)):
            if doy in spring:
                season.append('Spring')
            elif doy in summer:
                season.append('Summer')
            elif doy in fall:
                season.append('Fall')
            else:
                season.append('Winter')

        processed_dataframe['season'] = season
        processed_dataframe = processed_dataframe.join(pd.get_dummies(processed_dataframe['season'], prefix='season'))
        processed_dataframe.drop('season', axis=1, inplace=True)
        return processed_dataframe


    #Returns if the day is a weekday or not
    def get_weekday(self):
        processed_dataframe = self.get_season()

        weekday = []

        for day in range(len(processed_dataframe)):
            if processed_dataframe.iloc[day].name.weekday() < 5:
                weekday.append('Weekday')
            else:  # 5 Sat, 6 Sun
                weekday.append('Weekend')

        processed_dataframe['weekday'] = weekday
        processed_dataframe = processed_dataframe.join(pd.get_dummies(processed_dataframe['weekday'], prefix='weekday'))
        processed_dataframe.drop('weekday', axis=1, inplace=True)
        return processed_dataframe

    #Returns the period of the day for each row
    def get_period_day(self):

        processed_dataframe = self.get_weekday()
        period = []

        for day in range(len(processed_dataframe)):
            if 4 <= processed_dataframe.iloc[day].name.hour <= 11:
                period.append('Morning')
            elif 12 <= processed_dataframe.iloc[day].name.hour <= 19:
                period.append('Afternoon')
            else:
                period.append('Night')

        processed_dataframe['period'] = period
        processed_dataframe = processed_dataframe.join(pd.get_dummies(processed_dataframe['period'], prefix='period'))
        processed_dataframe.drop('period', axis=1, inplace=True)

        if self.target==None:
            return processed_dataframe
        else:
            merge = pd.merge(processed_dataframe,self.target,left_index=True, right_index=True)
            return merge
