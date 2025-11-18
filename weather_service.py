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


def check_weather_alerts(weather_data):
    """
    Check weather conditions against alert thresholds
    ALERT RULES FOR ST. JOHN'S:
    - Wind > 70 km/h → High wind warning (common in NL)
    - Visibility < 1 km → Fog alert (very common in St. John's)
    - Temperature < -20°C → Extreme cold warning
    - Temperature > 30°C → Heat warning (rare but possible)
    """
    
    alerts = []
    
    # Extract values from weather data
    wind_speed = weather_data["wind_speed"]
    visibility = weather_data["visibility"]
    temperature = weather_data["temperature"]
    
    # Check for high wind
    if wind_speed > 70:
        alerts.append({
            "type": "wind",
            "severity": "high",
            "message": f"⚠️ High wind warning! Current wind speed is {wind_speed} km/h. Secure loose objects and avoid unnecessary travel.",
            "current_value": wind_speed,
            "threshold": 70
        })
    
    # Check for fog (low visibility)
    if visibility < 1000:  # Less than 1 km
        visibility_km = round(visibility / 1000, 1)
        alerts.append({
            "type": "fog",
            "severity": "medium",
            "message": f"🌫️ Fog alert! Visibility is only {visibility_km} km. Drive carefully and use fog lights.",
            "current_value": visibility,
            "threshold": 1000
        })
    
    # Check for extreme cold
    if temperature < -20:
        alerts.append({
            "type": "cold",
            "severity": "high",
            "message": f"🥶 Extreme cold warning! Temperature is {temperature}°C. Frostbite risk - limit time outdoors.",
            "current_value": temperature,
            "threshold": -20
        })
    
    # Check for heat (rare in St. John's but possible)
    if temperature > 30:
        alerts.append({
            "type": "heat",
            "severity": "medium",
            "message": f"🌡️ Heat warning! Temperature is {temperature}°C. Stay hydrated and avoid prolonged sun exposure.",
            "current_value": temperature,
            "threshold": 30
        })
    
    # Check for moderate wind (warning, not emergency)
    elif wind_speed > 50:  # Between 50-70 km/h
        alerts.append({
            "type": "wind",
            "severity": "low",
            "message": f"💨 Windy conditions. Current wind speed is {wind_speed} km/h. Be cautious when driving.",
            "current_value": wind_speed,
            "threshold": 50
        })
    
    return alerts


def get_alert_summary(alerts):
    """ Create a human-readable summary of alerts """
    if not alerts:
        return "No severe weather alerts. Conditions are normal."
    
    # Count by severity
    high_count = len([a for a in alerts if a["severity"] == "high"])
    medium_count = len([a for a in alerts if a["severity"] == "medium"])
    low_count = len([a for a in alerts if a["severity"] == "low"])
    
    # Build summary
    summary_parts = []
    
    if high_count > 0:
        summary_parts.append(f"{high_count} severe warning(s)")
    if medium_count > 0:
        summary_parts.append(f"{medium_count} caution alert(s)")
    if low_count > 0:
        summary_parts.append(f"{low_count} advisory(s)")
    
    summary = "⚠️ Active alerts: " + ", ".join(summary_parts)
    
    return summary