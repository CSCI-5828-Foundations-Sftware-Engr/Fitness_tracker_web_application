import { render, screen } from '@testing-library/react';
import UserProfile from './UserProfile';
import { BrowserRouter as Router } from 'react-router-dom';

test('renders UserProfile component without errors', () => {
  render(
    <Router>
      <UserProfile name="John Doe" email="john.doe@example.com" contactNo="123-456-7890" />
    </Router>
  );
});

test('renders user information and update password form', () => {
  render(
    <Router>
      <UserProfile name="John Doe" email="john.doe@example.com" contactNo="123-456-7890" />
    </Router>
  );

  // Check if user information is rendered
  const nameElement = screen.getByText(/John Doe/i);
  const emailElement = screen.getByText(/john.doe@example.com/i);
  const contactNoElement = screen.getByText(/123-456-7890/i);
  expect(nameElement).toBeInTheDocument();
  expect(emailElement).toBeInTheDocument();
  expect(contactNoElement).toBeInTheDocument();

  // Check if update password form is rendered
  const newPasswordLabel = screen.getByLabelText(/New Password:/i);
  const confirmPasswordLabel = screen.getByLabelText(/Confirm New Password:/i);
  const updatePasswordButton = screen.getByRole('button', { name: /Update Password/i });
  expect(newPasswordLabel).toBeInTheDocument();
  expect(confirmPasswordLabel).toBeInTheDocument();
  expect(updatePasswordButton).toBeInTheDocument();
});
