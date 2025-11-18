from fastapi import FastAPI, HTTPException
from weather_service import fetch_current_weather, check_weather_alerts, get_alert_summary
from fastapi.middleware.cors import CORSMiddleware

# Create FastAPI app
app = FastAPI(title="St. John's Weather Alert System")

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {
        "message": "Welcome to St. John's Weather Alert System",
        "status": "running",
        "location": "St. John's, NL, Canada"
    }

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/weather")
def get_weather():
    try:
        weather_data = fetch_current_weather()
        return weather_data
    except Exception as e:
        # Return proper HTTP error if weather fetch fails
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/alerts")
def get_alerts():
    """ Get active weather alerts for St. John's """
    try:
        # Get current weather
        weather_data = fetch_current_weather()
        
        # Check for alerts
        alerts = check_weather_alerts(weather_data)
        
        # Get summary
        summary = get_alert_summary(alerts)
        
        # Return response
        return {
            "location": "St. John's, NL",
            "summary": summary,  # NEW!
            "current_conditions": {
                "temperature": weather_data["temperature"],
                "wind_speed": weather_data["wind_speed"],
                "visibility": weather_data["visibility"],
                "description": weather_data["description"]
            },
            "alert_count": len(alerts),
            "alerts": alerts
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/dashboard")
def get_dashboard():
    """ Get complete weather dashboard data """
    try:
        # Fetch weather
        weather_data = fetch_current_weather()
        
        # Check alerts
        alerts = check_weather_alerts(weather_data)
        
        # Get summary
        summary = get_alert_summary(alerts)
        
        # Return everything
        return {
            "location": "St. John's, NL",
            "weather": weather_data,
            "alerts": {
                "summary": summary,
                "count": len(alerts),
                "details": alerts
            },
            "timestamp": "now"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))