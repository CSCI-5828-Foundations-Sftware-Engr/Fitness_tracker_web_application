import { render, screen, fireEvent, getByPlaceholderText, getByRole, waitFor } from "@testing-library/react";
import LoginForm from "../LoginForm";

test('LoginForm has two tabs', () => {
  const { getByText } = render(<LoginForm />);
  const loginTab = getByText('Login');
  const signupTab = getByText('Signup');
  expect(loginTab).toBeInTheDocument();
  expect(signupTab).toBeInTheDocument();
});

test('clicking signup button sets active tab to signup', () => {
  const { getByText } = render(<LoginForm />);
  const signupButton = getByText("Signup");
  fireEvent.click(signupButton);
  expect(getByText("Signup")).toHaveClass("active");
});

test('form data updates when input values change', () => {
  const { getByPlaceholderText } = render(<LoginForm />);
  const usernameInput = getByPlaceholderText(/enter username/i);
  const passwordInput = getByPlaceholderText(/enter password/i);
  fireEvent.change(usernameInput, { target: { value: 'testuser' } });
  fireEvent.change(passwordInput, { target: { value: 'testpassword' } });
  expect(usernameInput).toHaveValue('testuser');
  expect(passwordInput).toHaveValue('testpassword');
});

test('login form data is submitted when form is submitted', async () => {
  const mockFetch = jest.fn();
  global.fetch = mockFetch;
  mockFetch.mockResolvedValueOnce({ json: jest.fn().mockResolvedValueOnce({ success: true }) });
  const { getByPlaceholderText, getByText } = render(<LoginForm />);
  const usernameInput = getByPlaceholderText(/enter username/i);
  const passwordInput = getByPlaceholderText(/enter password/i);
  const submitButton = getByText(/submit/i);
  fireEvent.change(usernameInput, { target: { value: 'testuser' } });
  fireEvent.change(passwordInput, { target: { value: 'testpassword' } });
  fireEvent.click(submitButton);
  await waitFor(() => expect(mockFetch).toHaveBeenCalledTimes(1));
  expect(mockFetch).toHaveBeenCalledWith('/login', expect.objectContaining({
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      username: 'testuser',
      password: 'testpassword'
    })
  }));
});

test('signup form data is submitted when form is submitted', async () => {
  const mockFetch = jest.fn();
  global.fetch = mockFetch;
  mockFetch.mockResolvedValueOnce({ json: jest.fn().mockResolvedValueOnce({ success: true }) });
  const { getByPlaceholderText, getByText } = render(<LoginForm />);
  const signupButton = getByText("Signup");
  fireEvent.click(signupButton);
  const usernameInput = getByPlaceholderText(/enter username/i);
  const passwordInput = getByPlaceholderText(/enter password/i);
  const emailInput = getByPlaceholderText(/enter email/i);
  const contactInput = getByPlaceholderText(/enter contact number/i);
  const submitButton = getByText(/register/i);
  fireEvent.change(usernameInput, { target: { value: 'testuser' } });
  fireEvent.change(passwordInput, { target: { value: 'testpassword' } });
  fireEvent.change(emailInput, { target: { value: 'test@abc.com' } });
  fireEvent.change(contactInput, { target: { value: '12345' } });
  fireEvent.click(submitButton);
  await waitFor(() => expect(mockFetch).toHaveBeenCalledTimes(1));
  expect(mockFetch).toHaveBeenCalledWith('/signup', expect.objectContaining({
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      username: 'testuser',
      password: 'testpassword',
      email: 'test@abc.com',
      contactNumber: '12345'
    })
  }));
});
 