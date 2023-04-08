import logo from "./logo-transparent-svg.svg";
import React, { useState } from "react";

const LoginForm = props => {
    const [activeTab, setActiveTab] = useState('login');
  
    const handleTabChange = tab => {
      setActiveTab(tab);
    };
  
    return (
      <div id="loginform">    
        <FormHeader activeTab={activeTab} handleTabChange={handleTabChange} />
        {activeTab === 'login' ? <LoginFormInput /> : <SignupFormInput />}
      </div>
    );
  };
  
  
  const FormHeader = props => {
    return (
      <div >
        <div className="form-header">
          <img src={logo} width={200} height={200} />
        </div>   
        <div className="tabs">
          <button
            className={props.activeTab === 'login' ? 'active' : ''}
            onClick={() => props.handleTabChange('login')}
          >
            Login
          </button>
          <button
            className={props.activeTab === 'signup' ? 'active' : ''}
            onClick={() => props.handleTabChange('signup')}
          >
            Signup
          </button>
        </div>
      </div>
    );
  };
  
  
  
  const LoginFormInput = props => (
    <div>
      <FormInput description="Username" placeholder="Enter Username" type="text" />
      <FormInput description="Password" placeholder="Enter Password" type="password" />
      <FormButton title="Submit" />
    </div>
  );
  
  const SignupFormInput = props => (
    <div>
      <FormInput description="Username" placeholder="Enter Username" type="text" />
      <FormInput description="Password" placeholder="Enter Password" type="password" />
      <FormInput description="Email" placeholder="Enter Email" type="email" />
      <FormInput description="Contact Numner" placeholder="Enter Contact Number" type="number" />
      <FormButton title="Register" />
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
  
  export default LoginForm;