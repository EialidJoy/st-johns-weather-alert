import requests
import os
from dotenv import load_dotenv

load_dotenv()

# Configuration
API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5"
ST_JOHNS_LAT = 47.5615
ST_JOHNS_LON = -52.7126


def fetch_current_weather():
    """ Fetch current weather for St. John's from OpenWeatherMap """
    # Check if API key exists
    if not API_KEY:
        raise Exception("API key not found. Please check your .env file")
    
    try:
        # Build the API URL
        url = f"{BASE_URL}/weather"
        
        # Parameters for the API request
        params = {
            "lat": ST_JOHNS_LAT,
            "lon": ST_JOHNS_LON,
            "appid": API_KEY,
            "units": "metric"
        }
        
        # Make the API request
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        # Get JSON data
        data = response.json()
        
        # Extract and return the important weather information
        return {
            "location": "St. John's, NL",
            "temperature": round(data["main"]["temp"], 1),
            "feels_like": round(data["main"]["feels_like"], 1),
            "conditions": data["weather"][0]["main"],
            "description": data["weather"][0]["description"],
            "wind_speed": round(data["wind"]["speed"] * 3.6, 1),  # m/s to km/h
            "humidity": data["main"]["humidity"],
            "visibility": data.get("visibility", 10000),
            "pressure": data["main"]["pressure"]
        }
        
    except requests.exceptions.Timeout:
        raise Exception("Weather API request timed out")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to fetch weather: {str(e)}")