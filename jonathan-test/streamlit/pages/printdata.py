import streamlit as st
import pandas as pd

#
# this is my print page
#

st.set_page_config(page_title='Print data',
                   layout="centered",
                   initial_sidebar_state="auto")

def print_data(data):
    weather_df = pd.read_csv(data, index_col=0)#[0:row]
    return weather_df

if st.button('see data set'):
    my_data = print_data('/home/jonathand/code/Johnny4good/electroprophet/jonathan-test/fastapi/data/df_amiens_weather.csv')
    st.bar_chart(data=my_data, y=['temperature_2m']) #'relativehumidity_2m'
