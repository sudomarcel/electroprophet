import streamlit as st
import time
import sys, os
import pandas as pd
from prophecy.get_data_forecast import WeatherForecast # step 2 below
from prophecy.main import main
# from prophecy.feature_processing import XXX # step 3 below
try:
    st.set_page_config(page_title='Recommendation',
                    layout="centered",
                    initial_sidebar_state="auto")


    # if st.button("Run the predictions"):
    #     st.markdown("Try our app")

    ####################################
    # STEP 1 :
    # GET USER INPUT (CITY NAME)
    #
    ####################################

    place = st.text_input(label="Enter a city:")

    df = main(place)
    st.dataframe(df)
    if st.button("Run the predictions"):
        st.dataframe(df)

    ####################################
    # STEP 2 :
    # GET WEATHER FORECAST FROM THE CITY
    #
    ####################################

    # def weather_forecast(place):
    #     """
    #     This function call the method get_weather_forecast()
    #     from the class prophecy.WeatherForecast
    #     and return the response from the weather API.
    #     """

    #     weather = WeatherForecast(place, 1)
    #     response = weather.get_weather_forecast()
    #     return response

    # if st.button("Run the predictions"):
    #     place_dict = weather_forecast(place)
    #     #wait()
    #     #show_recommendations()
    #     #df = pd.DataFrame([place_dict])
    #     st.markdown("Importing weather forecast from the city...")
    #     st.table(place_dict)

    ####################################
    # STEP 3 :
    # PREPROCESS THE DATA
    #
    ####################################




    ####################################
    # STEP 4 :
    # PREDICT WIND AND SUN ELECTRICITY
    # PRODUCTION WITH THE PREPROCESSED DATA
    #
    ####################################


    ####################################
    # STEP 5 :
    # PREDICT CONSUMPTION WITH THE PREPROCESSED DATA
    #
    ####################################



    ####################################
    # STEP 6 :
    # GIVE OUR RECOMMENDATION
    #
    ####################################

    img_link = {"bad_face" : 'https://cdn4.iconfinder.com/data/icons/aami-web-internet/64/aami13-41-1024.png',
                "neutral_face" : 'https://cdn4.iconfinder.com/data/icons/aami-web-internet/64/aami13-04-1024.png',
                "good_face" : 'https://cdn4.iconfinder.com/data/icons/aami-web-internet/64/aami13-46-1024.png'}
    
    # create a dictionary that maps each mood to the corresponding image file
    mood_to_image = {
    'Good': img_link['good_face'],
    'Bad': img_link['bad_face'],
    'Normal': img_link['neutral_face']}
    
    # use the map function to apply the mapping to the DataFrame
    df['image'] = df['recommendation'].map(mood_to_image)
    
    # set the number of columns and rows for the image grid
    num_cols = 4
    num_rows = 6

    # create the image grid using the beta_columns function
    col_list = st.beta_columns(num_cols)
    for i, col in enumerate(col_list):
        for j in range(num_rows):
            with col:
                # load the image for the current mood
                mood = df['recommendation'][num_rows*i+j]
                image_file = mood_to_image[mood]
                image = Image.open(image_file)

                # display the image on the Streamlit app
                st.image(image, width=100)

    # def show_recommendations():
    #     st.balloons()

    #     col_hours, col_d0, col_d1, col_d2 = st.columns(4)

    #     with col_hours:
    #         st.header("Time")

    #     with col_d0:
    #         st.header("Today")

    #     with col_d1:
    #         st.header("Tomorrow")

    #     with col_d2:
    #         st.header("After tomorrow")

    #     #
    #     # Morning
    #     #

    #     col_hours, col_d0, col_d1, col_d2 = st.columns(4)

    #     with col_hours:
    #         st.header("Morning")

    #     with col_d0:
    #         st.image(img_link['happy'])

    #     with col_d1:
    #         st.image(img_link['unhappy'])

    #     with col_d2:
    #         st.image(img_link['neutral'])

    #     #
    #     # Afternoon
    #     #

    #     col_hours, col_d0, col_d1, col_d2 = st.columns(4)

    #     with col_hours:
    #         st.header("Afternoon")

    #     with col_d0:
    #         st.image(img_link['happy'])

    #     with col_d1:
    #         st.image(img_link['unhappy'])

    #     with col_d2:
    #         st.image(img_link['neutral'])

    #     #
    #     # NIGHT
    #     #

    #     col_hours, col_d0, col_d1, col_d2 = st.columns(4)

    #     with col_hours:
    #         st.header("Night")

    #     with col_d0:
    #         st.image(img_link['happy'])

    #     with col_d1:
    #         st.image(img_link['unhappy'])

    #     with col_d2:
    #         st.image(img_link['neutral'])

    # def wait():
    #     with st.spinner("Wait, our model is reaching the stars for you..."):
    #         time.sleep(3)
    #         st.success("1/5...everything's gonna be alright ")

    #     with st.spinner("Updating API from API"):
    #         time.sleep(1.5)
    #         st.success("2/5...come on baby")

    #     with st.spinner("Preprocessing..."):
    #         time.sleep(1.5)
    #         st.success("3/5...i like it")

    #     with st.spinner("Fitting..."):
    #         time.sleep(1.5)
    #         st.success("4/5...just amazing")

    #     with st.spinner("Predicting..."):
    #         time.sleep(1.5)
    #         st.success("5/5...Maravilhoso")

    # if st.button("Run the predictions"):
    #     wait()
    #     show_recommendations()
except:
    pass
