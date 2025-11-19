import './App.css';
import { useState, useEffect } from 'react';
import axios from 'axios';

function App() {
  // State to store weather data
  const [weather, setWeather] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Fetch weather when component loads
  useEffect(() => {
    fetchWeather();
  }, []);

  const fetchWeather = async () => {
    try {
      setLoading(true);
      
      // Call your FastAPI backend
      const response = await axios.get('http://localhost:8000/weather');
      
      setWeather(response.data);
      setLoading(false);
      
    } catch (err) {
      setError(err.message);
      setLoading(false);
    }
  };

  // Show loading message
  if (loading) {
    return (
      <div className="App">
        <h1>St. John's Weather Alert System</h1>
        <p className='loading'>Loading weather data...</p>
      </div>
    );
  }

  // Show error if API call failed
  if (error) {
    return (
      <div className="App">
        <h1>St. John's Weather Alert System</h1>
        <p className='error'>Error: {error}</p>
        <button onClick={fetchWeather}>Try Again</button>
      </div>
    );
  }

  // Display weather data
  return (
    <div className="App">
      <h1>St. John's Weather Alert System</h1>
      
      {weather && (
        <div className='weather-container'>
          <h2>{weather.location}</h2>
          <p><strong>Temperature:</strong> {weather.temperature}°C</p>
          <p><strong>Feels Like:</strong> {weather.feels_like}°C</p>
          <p><strong>Conditions:</strong> {weather.conditions}</p>
          <p><strong>Description:</strong> {weather.description}</p>
          <p><strong>Wind Speed:</strong> {weather.wind_speed} km/h</p>
          <p><strong>Humidity:</strong> {weather.humidity}%</p>
          <p><strong>Visibility:</strong> {weather.visibility}m</p>
        </div>
      )}
      
      <button onClick={fetchWeather}>Refresh Weather</button>
    </div>
  );
}

export default App;