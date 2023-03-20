from prophecy.get_data_forecast import WeatherForecast
from prophecy.feature_processing import FeaturePreprocessing

class ForecastDataframe:
    def __init__(self, city):
        self.city = city

    def calling_the_other_classes(self):
        weather_df = WeatherForecast(self.city)
        weather_df_renamed = weather_df.rename_columns()

        process_data = FeaturePreprocessing(weather_df_renamed)
        processed_forecast = process_data.get_period_day()

        return processed_forecast

    def return_scaled_forecast(self):
        df = self.calling_the_other_classes()
        if 'season_Fall' not in df.columns:
            df.insert(32, 'season_Fall', 0)
        if 'season_Spring' not in df.columns:
            df.insert(33, 'season_Spring', 0)
        if 'season_Summer' not in df.columns:
            df.insert(34, 'season_Summer', 0)
        if 'season_Winter' not in df.columns:
            df.insert(35, 'season_Winter', 0)

        if 'weekday_Weekday' not in df.columns:
            df.insert(35, 'weekday_Weekday', 0)
        if 'weekday_Weekend' not in df.columns:
            df.insert(35, 'weekday_Weekend', 0)

        return df
