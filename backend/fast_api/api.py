from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

from prophecy.feature_processing import FeaturePreprocessing
import tensorflow as tf
from prophecy.get_data_forecast import WeatherForecast
app = FastAPI()

@app.get("/")
def index():
    return {"status": "ok"}

@app.get('/predict')
def predict(city, days):
    new_data = WeatherForecast(city, days)
    print(new_data)
    processed_data = FeaturePreprocessing(new_data).get_period_day()
    new_model = tf.keras.models.load_model('saved_model/my_model')

    print(new_model.summary())
    result = new_model.predict(new_data)

    return(result)
