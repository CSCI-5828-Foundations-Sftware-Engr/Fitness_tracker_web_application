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
      <div className="user-profile-circle">M</div>
      <p>Manali Kale {name}</p>
      <p>manali.kale@colorado.edu {email}</p>
      <p>+12346578901{contactNo}</p>

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
