import streamlit as st
import time

st.set_page_config(page_title='Recommendation',
                   layout="centered",
                   initial_sidebar_state="auto")


img_link = {"unhappy" : 'https://cdn4.iconfinder.com/data/icons/aami-web-internet/64/aami13-41-1024.png',
            "neutral" : 'https://cdn4.iconfinder.com/data/icons/aami-web-internet/64/aami13-04-1024.png',
            "happy" : 'https://cdn4.iconfinder.com/data/icons/aami-web-internet/64/aami13-46-1024.png'}


def show_recommendations():
    st.balloons()

    col_hours, col_d0, col_d1, col_d2 = st.columns(4)

    with col_hours:
        st.header("Time")

    with col_d0:
        st.header("Today")

    with col_d1:
        st.header("Tomorrow")

    with col_d2:
        st.header("After tomorrow")

    #
    # Morning
    #

    col_hours, col_d0, col_d1, col_d2 = st.columns(4)

    with col_hours:
        st.header("Morning")

    with col_d0:
        st.image(img_link['happy'])

    with col_d1:
        st.image(img_link['unhappy'])

    with col_d2:
        st.image(img_link['neutral'])

    #
    # Afternoon
    #

    col_hours, col_d0, col_d1, col_d2 = st.columns(4)

    with col_hours:
        st.header("Afternoon")

    with col_d0:
        st.image(img_link['happy'])

    with col_d1:
        st.image(img_link['unhappy'])

    with col_d2:
        st.image(img_link['neutral'])

    #
    # NIGHT
    #

    col_hours, col_d0, col_d1, col_d2 = st.columns(4)

    with col_hours:
        st.header("Night")

    with col_d0:
        st.image(img_link['happy'])

    with col_d1:
        st.image(img_link['unhappy'])

    with col_d2:
        st.image(img_link['neutral'])

def wait():
    with st.spinner("Wait, our model is reaching the stars for you..."):
        time.sleep(3)
        #st.success("1/5...everything's gonna be alright ")

    with st.spinner("Updating API from API"):
        time.sleep(1.5)
        st.success("2/5...come on baby")

    with st.spinner("Preprocessing..."):
        time.sleep(1.5)
        st.success("3/5...i like it")

    with st.spinner("Fitting..."):
        time.sleep(1.5)
        st.success("4/5...just amazing")

    with st.spinner("Predicting..."):
        time.sleep(1.5)
        st.success("5/5...Maravilhoso")

if st.button("Run the predictions"):
    wait()
    show_recommendations()
