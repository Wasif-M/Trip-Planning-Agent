import json
import requests
import os
from dotenv import load_dotenv
load_dotenv()

def get_day_weather_forecast(location: str, days: int) -> dict:
    """
    Fetch the next 'days' of real-time weather for the given location using WeatherAPI.com.
    Args:
        location (str): The location (city name, coordinates, etc.)
        days (int): Number of days for the forecast (1-10)
    Returns:
        dict: Weather forecast data for the specified number of days.
    """
    api_key = os.environ.get("WEATHER_API_KEY")
    if not api_key:
        return {"error": "WEATHER_API_KEY environment variable not set."}
    url = f"https://api.weatherapi.com/v1/forecast.json?key={api_key}&q={location}&days={days}&aqi=no&alerts=no"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Failed to fetch weather data: {response.status_code} - {response.text}"}