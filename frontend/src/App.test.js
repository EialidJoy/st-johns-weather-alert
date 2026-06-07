import { render, screen } from '@testing-library/react';
import App from './App';

beforeEach(() => {
  global.fetch = jest.fn(() =>
    Promise.resolve({
      ok: true,
      json: () =>
        Promise.resolve({
          location: "St. John's, NL",
          weather: {
            temperature: 5,
            feels_like: 2,
            conditions: 'Clouds',
            description: 'overcast clouds',
            wind_speed: 30,
            humidity: 80,
            visibility: 10000,
            pressure: 1013,
          },
          alerts: {
            summary: 'No severe weather alerts. Conditions are normal.',
            count: 0,
            details: [],
          },
        }),
    })
  );
});

test('renders app title', async () => {
  render(<App />);
  expect(screen.getByText(/St\. John's Weather Alert/i)).toBeInTheDocument();
});
