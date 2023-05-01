// GoalTracker.test.js
import { render, screen } from '@testing-library/react';
import GoalTracker from './GoalTracker';

test('renders goal tracker component with form elements', () => {
  render(<GoalTracker />);
  const formHeader = screen.getByText(/Set your Goals/i);
  expect(formHeader).toBeInTheDocument();

  const currentWeightInput = screen.getByLabelText(/Current weight:/i);
  const targetWeightInput = screen.getByLabelText(/Targeted weight:/i);
  const ageInput = screen.getByLabelText(/Age:/i);
  const heightInput = screen.getByLabelText(/Height:/i);
  const targetStepsInput = screen.getByLabelText(/Target no. of steps:/i);
  const targetDistanceInput = screen.getByLabelText(/Distance to walk or run:/i);
  const waterGoalInput = screen.getByLabelText(/Water Goal (in glasses):/i);
  const caloriesGoalInput = screen.getByLabelText(/Target Calories to Burn:/i);

  expect(currentWeightInput).toBeInTheDocument();
  expect(targetWeightInput).toBeInTheDocument();
  expect(ageInput).toBeInTheDocument();
  expect(heightInput).toBeInTheDocument();
  expect(targetStepsInput).toBeInTheDocument();
  expect(targetDistanceInput).toBeInTheDocument();
  expect(waterGoalInput).toBeInTheDocument();
  expect(caloriesGoalInput).toBeInTheDocument();

  const submitButton = screen.getByRole('button', { name: /Submit/i });
  expect(submitButton).toBeInTheDocument();
});
