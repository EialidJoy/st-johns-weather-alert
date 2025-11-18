from fastapi import FastAPI
from weather_service import fetch_current_weather
from fastapi.middleware.cors import CORSMiddleware

# Create FastAPI app
app = FastAPI(title="St. John's Weather Alert System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root endpoint
@app.get("/")
def home():
    return {
        "message": "Welcome to St. John's Weather Alert System",
        "status": "running",
        "location": "St. John's, NL, Canada"
    }

# Health check endpoint
@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/weather")
def get_weather():
    return fetch_current_weather()