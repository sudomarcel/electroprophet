import streamlit as st
import pandas as pd

#
# this is my home page
#

st.set_page_config(page_title='Home page',
                   layout="centered",
                   initial_sidebar_state="auto",
                   menu_items={
                       'Get Help': 'https://www.extremelycoolapp.com/help',
                       'About': "# This is a header. This is an *extremely* cool app!"
                                }
                )

def intro():
    import streamlit as st
    st.write('Welcome to my home page')
    st.markdown("""
                Our project was made to analyse data from electricity
                production from the wind and the sun. Our model compute
                prediction
                of the electricity production that will help you
                to reduce your carbon footprint.
                """)

    st.sidebar.success('What would you like to do ?')

intro()
