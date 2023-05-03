import { render, screen } from '@testing-library/react';
import LoginForm from '../LoginForm';

test('renders login form component', () => {
  render(<LoginForm />);
});

test('renders correct form header and active tab', () => {
  render(<LoginForm />);
  const formHeader = screen.getByText(/login/i);
  const activeTab = screen.getByRole('button', { name: /login/i });
  expect(formHeader).toBeInTheDocument();
  expect(activeTab).toHaveClass('active');
});
