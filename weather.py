"""
weather.py
Handles all OpenWeatherMap API interactions.
"""
import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


def get_weather(city: str) -> dict:
    """
    Fetch current weather for a city.
    Returns a clean dict with what we care about, or raises an exception.
    """
    if not API_KEY:
        raise ValueError("OPENWEATHER_API_KEY not set in .env file")

    try:
        response = requests.get(
            BASE_URL,
            params={
                "q": city,
                "appid": API_KEY,
                "units": "metric"   # Celsius. Use "imperial" for Fahrenheit.
            },
            timeout=10
        )
        response.raise_for_status()
        raw = response.json()

        # Extract just what we need (clean output)
        return {
            "city": raw["name"],
            "country": raw["sys"]["country"],
            "temp": raw["main"]["temp"],
            "feels_like": raw["main"]["feels_like"],
            "humidity": raw["main"]["humidity"],
            "description": raw["weather"][0]["description"].title(),
            "wind_speed": raw["wind"]["speed"],
        }

    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 401:
            raise ValueError("Invalid OpenWeather API key (or wait 10 mins after signup)")
        elif e.response.status_code == 404:
            raise ValueError(f"City '{city}' not found")
        raise

    except requests.exceptions.Timeout:
        raise TimeoutError("OpenWeather request timed out")