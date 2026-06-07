const SEVERITY_STYLES = {
  high: 'alert-high',
  medium: 'alert-medium',
  low: 'alert-low',
};

const TYPE_ICONS = {
  wind: '💨',
  fog: '🌫️',
  cold: '🥶',
  heat: '🌡️',
};

function AlertDisplay({ alerts, summary }) {
  if (!alerts || alerts.length === 0) {
    return (
      <section className="alerts-section">
        <h2>Weather Alerts</h2>
        <div className="alert-card all-clear">
          <span className="alert-icon">✅</span>
          <p>{summary || 'No severe weather alerts. Conditions are normal.'}</p>
        </div>
      </section>
    );
  }

  return (
    <section className="alerts-section">
      <h2>Weather Alerts</h2>
      <p className="alert-summary">{summary}</p>
      <div className="alerts-list">
        {alerts.map((alert, index) => (
          <div
            key={`${alert.type}-${index}`}
            className={`alert-card ${SEVERITY_STYLES[alert.severity] || ''}`}
          >
            <div className="alert-header">
              <span className="alert-icon">{TYPE_ICONS[alert.type] || '⚠️'}</span>
              <span className={`severity-badge severity-${alert.severity}`}>
                {alert.severity}
              </span>
            </div>
            <p className="alert-message">{alert.message}</p>
          </div>
        ))}
      </div>
    </section>
  );
}

export default AlertDisplay;
