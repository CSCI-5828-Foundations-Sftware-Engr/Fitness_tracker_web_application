import { render, screen } from '@testing-library/react';
import Dashboard from '../Dashboard';
import { BrowserRouter as Router } from 'react-router-dom';

test('renders Dashboard component without errors', () => {
  render(
    <Router>
      <Dashboard />
    </Router>
  );
});

test('renders Header and SideMenu components', () => {
  render(
    <Router>
      <Dashboard />
    </Router>
  );

  // Check if the Header component is rendered
  const headerElement = screen.getByTestId('header');
  expect(headerElement).toBeInTheDocument();

  // Check if the SideMenu component is rendered
  const sideMenuElement = screen.getByTestId('side-menu');
  expect(sideMenuElement).toBeInTheDocument();
});
