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

st.markdown("<h1 style='text-align: center; color: red;'>Homepage</h1>", unsafe_allow_html=True)

intro()

img_link = {"unhappy" : '/home/jonathand/code/Johnny4good/electroprophet/jonathan-test/streamlit/images/face_unhappy.png',
            "neutral" : '/home/jonathand/code/Johnny4good/electroprophet/jonathan-test/streamlit/images/face_neutral.png',
            "happy" : '/home/jonathand/code/Johnny4good/electroprophet/jonathan-test/streamlit/images/face_happy.png'}


col0, col1, col2, col3 = st.columns(4)

img_width = 100

with col0:
    st.header("H+1")
    st.image(img_link['happy'], width=img_width)
    st.write('')
    st.header("H+4")
    st.image(img_link['unhappy'], width=img_width)


with col1:
    st.header("H+2")
    st.image(img_link['neutral'], width=img_width)
    st.write('')
    st.header("H+6")
    st.image(img_link['unhappy'], width=img_width)

with col2:
    st.header("H+3")
    st.image(img_link['happy'], width=img_width)
    st.write('')
    st.header("H+7")
    st.image(img_link['unhappy'], width=img_width)

with col3:
    st.header("H+4")
    st.image(img_link['neutral'], width=img_width)
    st.write('')
    st.header("H+8")
    st.image(img_link['neutral'], width=img_width)

#st.image('streamlit/images/Contact-us.png', width=150)
