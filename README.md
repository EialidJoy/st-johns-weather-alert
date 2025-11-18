# St. John's Weather Alert System

Real-time weather monitoring and alert system for St. John's, Newfoundland and Labrador.

## ✅ Completed Features
- ✅ Real-time weather data for St. John's
- ✅ Automatic alert detection (wind, fog, temperature)
- ✅ Severity levels (high, medium, low)
- ✅ API documentation at /docs

## 🚧 Coming Soon
- React dashboard (Week 3)
- 5-day forecast
- Email notifications

## Tech Stack
- **Backend:** Python, FastAPI
- **Weather API:** OpenWeatherMap
- **Frontend:** React (coming soon)

## API Endpoints

### GET /weather
Returns current weather conditions

### GET /alerts
Returns active weather alerts with severity levels

### GET /dashboard
Returns complete weather + alerts data (single call)

### GET /docs
Interactive API documentation

## Alert Thresholds
- **High Wind:** > 70 km/h
- **Fog:** Visibility < 1 km
- **Extreme Cold:** < -20°C
- **Heat:** > 30°C

## Setup

1. Clone repository
```bash
git clone https://github.com/YOUR_USERNAME/st-johns-weather-alert.git
cd st-johns-weather-alert
```

2. Install dependencies
```bash
pip install fastapi uvicorn requests python-dotenv
```

3. Create `.env` file
```
OPENWEATHER_API_KEY=your_key_here
```

4. Run application
```bash
uvicorn main:app --reload
```

5. Visit http://localhost:8000/docs

## Developer
[Your Name] - St. John's, NL

## Progress
✅ Week 1 Complete - Backend with weather alerts working!