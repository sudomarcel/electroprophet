import pandas as pd
import numpy as np

def get_wind_components(df_scaled: pd.DataFrame) -> np.ndarray:

    # Convert degrees to radians and store the values into wd_rad
    #wind direction 10 m
    wd_rad_10 = df_scaled.pop('winddirection_10m')*np.pi / 180

    #wind direction 100 m
    wd_rad_100 = df_scaled.pop('winddirection_100m')*np.pi / 180

    # Calculate the wind x and y components and store then in two new columns
    # `Wx` and `Wy`
    #wind speed 10 m
    wv_10 = df_scaled.pop('windspeed_10m')
    df_scaled['Wx_10'] = wv_10*np.cos(wd_rad_10)
    df_scaled['Wy_10'] = wv_10*np.sin(wd_rad_10)

    #wind speed 100 m
    wv_100 = df_scaled.pop('windspeed_100m')
    df_scaled['Wx_100'] = wv_10*np.cos(wd_rad_100)
    df_scaled['Wy_100'] = wv_10*np.sin(wd_rad_100)

    return df_scaled


