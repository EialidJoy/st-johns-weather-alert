from fastapi import FastAPI, HTTPException
from weather_service import fetch_current_weather
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