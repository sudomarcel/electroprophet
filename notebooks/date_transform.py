import pandas as pd
import numpy as np
from datetime import datetime, date
from dateutil.relativedelta import relativedelta


#Get season function
def get_season(df_scaled: pd.DataFrame) -> np.ndarray:
    """
    Calls a function data gets the day from the time column,
    outputs whether the day is in the Spring, Summer, Fall or
    Winter and creates 
    """
    
    season = []

    # get the current day of the year
    doy = df_scaled.iloc[0].name.timetuple().tm_yday

    # "day of year" ranges for the northern hemisphere
    spring = range(80, 172)
    summer = range(172, 264)
    fall = range(264, 355)
    # winter = everything else

    for doy in range(len(df_scaled)):
        if doy in spring:
            season.append('Spring')
        elif doy in summer:
            season.append('Summer')
        elif doy in fall:
            season.append('Fall')
        else:
            season.append('Winter')

    df_scaled['season'] = season
    df_scaled = df_scaled.join(pd.get_dummies(df_scaled['season'], prefix='season'))
    df_scaled.drop('period', axis=1, inplace=True)
    return df_scaled


#Returns if the day is a weekday or not
def get_weekday(df_scaled: pd.DataFrame) -> np.ndarray:
    weekday = []
    
    for day in range(len(df_scaled)):
        if df_scaled.iloc[day].name.weekday() < 5:
            weekday.append('Weekday')
        else:  # 5 Sat, 6 Sun
            weekday.append('Weekend')
    
    df_scaled['weekday'] = weekday
    df_scaled = df_scaled.join(pd.get_dummies(df_scaled['weekday'], prefix='weekday'))
    df_scaled.drop('weekday', axis=1, inplace=True)
    return df_scaled


#Returns the period of the day for each row
def get_period_day(df_scaled: pd.DataFrame) -> pd.DataFrame:
    period = []
    
    for day in range(len(df_scaled)):
        if 4 <= df_scaled.iloc[day].name.hour <= 11:
            period.append('Morning')
        elif 12 <= df_scaled.iloc[day].name.hour <= 19:
            period.append('Afternoon')
        else:
            period.append('Night')
    
    df_scaled['period'] = period
    df_scaled = df_scaled.join(pd.get_dummies(df_scaled['period'], prefix='period'))
    df_scaled.drop('period', axis=1, inplace=True)
    return df_scaled