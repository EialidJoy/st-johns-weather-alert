import os

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from weather_service import fetch_current_weather, check_weather_alerts, get_alert_summary

# Create FastAPI app
app = FastAPI(title="St. John's Weather Alert System")

# Enable CORS for the React dev server (production is same-origin, so this is
# only needed when running the frontend separately on port 3000).
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
def health():
    return {"status": "healthy"}


@app.get("/api/weather")
def get_weather():
    try:
        weather_data = fetch_current_weather()
        return weather_data
    except Exception as e:
        # Return proper HTTP error if weather fetch fails
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/alerts")
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
            "summary": summary,
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


@app.get("/api/dashboard")
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


# Serve the built React app (single-service production deploy). Mounted last so
# it never shadows the /api routes above. Only mounted when a build exists, so
# local development (frontend on port 3000) is unaffected.
BUILD_DIR = os.path.join(os.path.dirname(__file__), "frontend", "build")
if os.path.isdir(BUILD_DIR):
    app.mount("/", StaticFiles(directory=BUILD_DIR, html=True), name="frontend")
