from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

from get_data import WeatherEnergy
from feature_processing import FeaturePreprocessing
import tensorflow as tf

app = FastAPI()

# # Allow all requests (optional, good for development purposes)
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # Allows all origins
#     allow_credentials=True,
#     allow_methods=["*"],  # Allows all methods
#     allow_headers=["*"],  # Allows all headers
# )

@app.get("/")
def index():
    return {"status": "ok"}

@app.post('/predict')
async def predict(img: UploadFile=File(...)):

    #df = WeatherEnergy(
    #    limit=-1, offset=0, refine='Hauts-de-France', city=['Heudicourt', 'Bucy-les-Pierrepont', 'Riencourt'], years=10, target='eolien'
    #    ).merged()
    #df_processed = FeaturePreprocessing(df).get_period_day()

    new_data = FeaturePreprocessing(new_data).get_period_day()

    new_model = tf.keras.models.load_model('saved_model/my_model')

    print(new_model.summary())
    result = new_model.predict(new_data)

    return(result)
