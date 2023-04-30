import React, { useState } from 'react';

const UserProfile = (props) => {
  const [name, setName] = useState(props.name);
  const [email, setEmail] = useState(props.email);
  const [contactNo, setContactNo] = useState(props.contactNo);
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');

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
      <h2>User Profile</h2>
      <p>Name: {name}</p>
      <p>Email: {email}</p>
      <p>Contact No.: {contactNo}</p>

      <h3>Update Password</h3>
      <form className="update-password-form" onSubmit={handlePasswordUpdate}>
        <label htmlFor="password">New Password:</label>
        <input
          id="password"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />

        <label htmlFor="confirmPassword">Confirm New Password:</label>
        <input
          id="confirmPassword"
          type="password"
          value={confirmPassword}
          onChange={(e) => setConfirmPassword(e.target.value)}
        />

        <button type="submit">Update Password</button>
      </form>
    </div>
  );
};

export default UserProfile;
