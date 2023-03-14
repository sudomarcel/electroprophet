import streamlit as st
import requests

st.markdown("""# Welcome to my maravilhoso page
""")

url = 'http://127.0.0.1:8000/'

response = requests.get(url)

result = response.json()

st.header(result)
