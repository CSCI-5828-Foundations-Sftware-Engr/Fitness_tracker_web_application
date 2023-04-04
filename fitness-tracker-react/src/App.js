import './App.css';
import React, { useState } from "react";
import logo from "./logo-transparent-svg.svg";

function App() {
  return (
    <div class="mainPage">
      <LoginForm />
    </div>
  );
}

const LoginForm = props => (
  <div id="loginform">
    <FormHeader title="Fitness-Tracker-Application" />
    <Form />
  </div>
);

const FormHeader = props => {
  const [activeTab, setActiveTab] = useState('login');

  const handleTabChange = tab => {
    setActiveTab(tab);
  };

  return (
    <div >
      <div class="form-header">
      <img src={logo} width={200} height={200} />
      </div>   
      <div className="tabs">
        <button
          className={activeTab === 'login' ? 'active' : ''}
          onClick={() => handleTabChange('login')}
        >
          Login
        </button>
        <button
          className={activeTab === 'signup' ? 'active' : ''}
          onClick={() => handleTabChange('signup')}
        >
          Signup
        </button>
      </div>
    </div>
  );
};



const Form = props => (
  <div>
    <FormInput description="Username" placeholder="Enter Username" type="text" />
    <FormInput description="Password" placeholder="Enter Password" type="password" />
    <FormButton title="Submit" />
  </div>
);

const FormButton = props => {
  const [response, setResponse] = React.useState('');
  const postData = () => {
    
    const username = document.querySelector('input[type="text"]').value;
    const password = document.querySelector('input[type="password"]').value;

    fetch('/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        username: username,
        password: password
      })
    })
    .then(response => response.json())
    .then(data => {console.log(data); setResponse(data)})
    .catch(error => console.error(error));
  }

  return (
    <div>
      <div id="button" class="row" onClick={postData}>
        <button>{props.title}</button>
      </div>
    </div>
  );
}

const FormInput = props => (
  <div class="row">
    <label>{props.description}</label>
    <input type={props.type} placeholder={props.placeholder} />
  </div>
);

export default App;