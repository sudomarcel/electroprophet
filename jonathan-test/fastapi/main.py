from fastapi import FastAPI
import matplotlib.pyplot as plt
import pandas as pd

app = FastAPI()

@app.get("/")
def index():
    return {"status": "ok"}

@app.get("/printdata")
def print_data():
    data = 'data/df_amiens_weather.csv'
    weather_df = pd.read_csv(data, index_col=0)#[0:row]
    return weather_df

@app.get("/questions")
def load_questions():
    return print_data().to_dict(orient="records")
