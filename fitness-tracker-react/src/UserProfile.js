import React, { useContext, useState } from 'react';
import { useLocation } from 'react-router-dom';

const UserProfile = (props) => {
  const [name, setName] = useState(props.name);
  const [email, setEmail] = useState(props.email);
  const [contactNo, setContactNo] = useState(props.contactNo);
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const location = useLocation();
  const user = location.state;

  const handlePasswordUpdate = (e) => {
    e.preventDefault();
    if (password === confirmPassword) {
      // Handle password update logic here
      alert('Password updated successfully');
    } else {
      alert('Passwords do not match');
    }
  };

  return (
    <div className="user-profile-container">
      <div class="user-profile-circle">{user?.username.slice(0,1).toUpperCase()}</div>
      <p>{user?.username}</p>
      <p>{user?.email}</p>
      <p>{user?.contactNumber}</p>

      <h3>Update Password</h3>
      <form className="update-password-form" onSubmit={handlePasswordUpdate}>
        <div class="row">
        <label htmlFor="password">New Password:</label>
        <input
          id="password"
          type="password"
          placeholder="Enter Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />

        </div>
        <div class="row">

        <label htmlFor="confirmPassword">Confirm New Password:</label>
        <input
          id="confirmPassword"
          type="password"
          placeholder="Enter Password"
          value={confirmPassword}
          onChange={(e) => setConfirmPassword(e.target.value)}
        />
        </div>

        <button type="submit">Update Password</button>
      </form>
    </div>
  );
};

export default UserProfile;
