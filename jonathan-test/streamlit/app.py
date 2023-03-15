import streamlit as st
import requests
import pandas as pd
import numpy as np
# import fastapi as fastAPI
# from fastapi import main #folder name 'fasapi'

st.markdown("""# Welcome to ElectroProphet app ⚡
""")
rows = st.number_input('nomber of rows ', min_value=0, max_value=300, step=10, value=5)

chart_data = pd.DataFrame(np.random.rand(20, 3), columns=['a', 'b', 'c'])

data = pd.read_csv('/home/jonathand/code/Johnny4good/electroprophet/jonathan-test/fastapi/data/df_amiens_weather.csv')

st.write(data)
st.bar_chart(chart_data)

#with open('../data/df_amiens_weather.csv', 'r') as file:
#    st.bar_chart(data=file, x=, y=['temperature_2m', 'relativehumidity_2m'])

url = 'http://127.0.0.1:8000/questions'

response = requests.get(url)

result = response.json()

st.dataframe(result)
