// SideMenu.test.js
import { render, screen, fireEvent } from '@testing-library/react';
import { BrowserRouter as Router } from 'react-router-dom';
import SideMenu from './SideMenu';

test('renders side menu with menu items and default selected component', () => {
  render(
    <Router>
      <SideMenu />
    </Router>
  );

  // Check if the side menu is rendered
  const sideMenu = screen.getByTestId('side-menu');
  expect(sideMenu).toBeInTheDocument();

  // Check if all menu items are rendered
  const profileMenuItem = screen.getByText(/Profile/i);
  const goalMenuItem = screen.getByText(/Goal Tracking/i);
  const workoutMenuItem = screen.getByText(/Workout/i);
  const nutritionMenuItem = screen.getByText(/Nutrition/i);
  const logoutMenuItem = screen.getByText(/Logout/i);
  expect(profileMenuItem).toBeInTheDocument();
  expect(goalMenuItem).toBeInTheDocument();
  expect(workoutMenuItem).toBeInTheDocument();
  expect(nutritionMenuItem).toBeInTheDocument();
  expect(logoutMenuItem).toBeInTheDocument();

  // Check if the default selected component is GoalTracker
  const goalTrackerComponent = screen.getByText(/Current weight/i);
  expect(goalTrackerComponent).toBeInTheDocument();
});

test('clicking on menu items updates the selected component', () => {
  render(
    <Router>
      <SideMenu />
    </Router>
  );

  // Click on the UserProfile menu item and check if UserProfile component is rendered
  const profileMenuItem = screen.getByText(/Profile/i);
  fireEvent.click(profileMenuItem);
  const userProfileComponent = screen.getByText(/Update Password/i);
  expect(userProfileComponent).toBeInTheDocument();

  // Click on the Nutrition menu item and check if Nutrition component is rendered
  const nutritionMenuItem = screen.getByText(/Nutrition/i);
  fireEvent.click(nutritionMenuItem);
  const nutritionComponent = screen.getByText(/Nutrition component/i); // Update this with actual text from Nutrition component
  expect(nutritionComponent).toBeInTheDocument();

  // Click on the Workout menu item and check if Workout component is rendered
  const workoutMenuItem = screen.getByText(/Workout/i);
  fireEvent.click(workoutMenuItem);
  const workoutComponent = screen.getByText(/Workout component/i); // Update this with actual text from Workout component
  expect(workoutComponent).toBeInTheDocument();
});
