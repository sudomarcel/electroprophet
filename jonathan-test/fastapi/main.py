from fastapi import FastAPI
import matplotlib.pyplot as plt
import pandas as pd
from prophecy.main import main
import sys
import os
sys.path.append('../')

app = FastAPI()

@app.get("/")
def index(city:str):
    prophecy = main(city)
    return {"result": prophecy}
