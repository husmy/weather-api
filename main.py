from fastapi import FastAPI, Query
import requests
import os
from dotenv import load_dotenv
from typing import Literal  
# Load the API key from .env file
load_dotenv()
API_KEY = os.getenv("WEATHER_API_KEY")

app = FastAPI()


@app.get("/")
def home():
    return {"message": "Welcome to the Weather API"} 

# Weather endpoint
@app.get("/weather")
def get_weather(
    city: str = Query(..., description="Enter a city name, e.g. 'London' or 'Colombo'"),
    units: Literal["metric", "imperial"] = Query("metric", description="Units: 'metric' = Celsius, 'imperial' = Fahrenheit")
):   
    # Request weather data from Openweathermap
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units={units}"
    response = requests.get(url)

    if response.status_code != 200:
        return {"error": "Could not fetch weather data", "details": response.json()}

    data = response.json()
    # Tranforming data received to weather to be returned 
    weather = {
        "city": data["name"],
        "country": data["sys"]["country"],
        "temperature": f"{data['main']['temp']} °{'C' if units == 'metric' else 'F'}", 
        "condition": data["weather"][0]["description"],
        "humidity": f"{data['main']['humidity']}%",
        "wind_speed": f"{data['wind']['speed']} {'m/s' if units == 'metric' else 'mph'}",
        "units": units
    }
    return weather

