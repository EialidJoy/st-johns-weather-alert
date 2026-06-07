const CONDITION_ICONS = {
  Clear: '☀️',
  Clouds: '☁️',
  Rain: '🌧️',
  Drizzle: '🌦️',
  Thunderstorm: '⛈️',
  Snow: '❄️',
  Mist: '🌫️',
  Fog: '🌫️',
  Haze: '🌫️',
};

function formatVisibility(meters) {
  if (meters >= 1000) {
    return `${(meters / 1000).toFixed(1)} km`;
  }
  return `${meters} m`;
}

function WeatherCard({ weather }) {
  const icon = CONDITION_ICONS[weather.conditions] || '🌤️';

  return (
    <section className="weather-section">
      <div className="weather-hero">
        <span className="weather-icon" aria-hidden="true">{icon}</span>
        <div className="weather-primary">
          <p className="temperature">{weather.temperature}°C</p>
          <p className="conditions">{weather.conditions}</p>
          <p className="description">{weather.description}</p>
        </div>
      </div>

      <div className="weather-stats">
        <div className="stat">
          <span className="stat-label">Feels like</span>
          <span className="stat-value">{weather.feels_like}°C</span>
        </div>
        <div className="stat">
          <span className="stat-label">Wind</span>
          <span className="stat-value">{weather.wind_speed} km/h</span>
        </div>
        <div className="stat">
          <span className="stat-label">Humidity</span>
          <span className="stat-value">{weather.humidity}%</span>
        </div>
        <div className="stat">
          <span className="stat-label">Visibility</span>
          <span className="stat-value">{formatVisibility(weather.visibility)}</span>
        </div>
        <div className="stat">
          <span className="stat-label">Pressure</span>
          <span className="stat-value">{weather.pressure} hPa</span>
        </div>
      </div>
    </section>
  );
}

export default WeatherCard;
