import { useState, useEffect, useCallback } from 'react';
import './App.css';
import WeatherCard from './WeatherCard';
import AlertDisplay from './AlertDisplay';

// Empty string = same-origin requests in production (FastAPI serves this build).
// In local dev, CRA's "proxy" in package.json forwards /api to localhost:8000.
const API_URL = process.env.REACT_APP_API_URL || '';
const REFRESH_INTERVAL_MS = 5 * 60 * 1000;

function App() {
  const [dashboard, setDashboard] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [lastUpdated, setLastUpdated] = useState(null);

  const fetchDashboard = useCallback(async () => {
    try {
      setError(null);
      const response = await fetch(`${API_URL}/api/dashboard`);

      if (!response.ok) {
        const body = await response.json().catch(() => ({}));
        throw new Error(body.detail || `Request failed (${response.status})`);
      }

      const data = await response.json();
      setDashboard(data);
      setLastUpdated(new Date());
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchDashboard();
    const interval = setInterval(fetchDashboard, REFRESH_INTERVAL_MS);
    return () => clearInterval(interval);
  }, [fetchDashboard]);

  if (loading) {
    return (
      <div className="app">
        <header className="app-header">
          <h1>St. John's Weather Alert</h1>
          <p className="subtitle">Newfoundland &amp; Labrador</p>
        </header>
        <p className="status-message loading">Loading weather data…</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="app">
        <header className="app-header">
          <h1>St. John's Weather Alert</h1>
          <p className="subtitle">Newfoundland &amp; Labrador</p>
        </header>
        <div className="error-panel">
          <p className="status-message error">Could not load weather data</p>
          <p className="error-detail">{error}</p>
          <p className="error-hint">Make sure the backend is running on port 8000.</p>
          <button type="button" onClick={fetchDashboard}>Try again</button>
        </div>
      </div>
    );
  }

  return (
    <div className="app">
      <header className="app-header">
        <h1>St. John's Weather Alert</h1>
        <p className="subtitle">{dashboard.location}</p>
        {lastUpdated && (
          <p className="last-updated">
            Updated {lastUpdated.toLocaleTimeString()}
          </p>
        )}
      </header>

      <main className="dashboard">
        <WeatherCard weather={dashboard.weather} />
        <AlertDisplay
          alerts={dashboard.alerts.details}
          summary={dashboard.alerts.summary}
        />
      </main>

      <footer className="app-footer">
        <button type="button" onClick={fetchDashboard}>Refresh</button>
      </footer>
    </div>
  );
}

export default App;
