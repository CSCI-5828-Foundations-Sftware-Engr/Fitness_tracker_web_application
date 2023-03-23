import './App.css';
import React, { useState } from "react";

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

const FormHeader = props => (
  <h2 id="headerTitle">{props.title}</h2>
);


const Form = props => (
  <div>
    <FormInput description="Calorie Intake" placeholder="Enter Calorie intake" type="number" />
    <FormInput description="Calories Burnt" placeholder="Enter Calories burnt" type="text" />
    <FormButton title="Submit" />
  </div>
);

const FormButton = props => {
  const [response, setResponse] = React.useState('');
  const postData = () => {
    
    const calorie_intake = document.querySelector('input[type="number"]').value;
    const calorie_burnt = document.querySelector('input[type="text"]').value;

    fetch('/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        calorie_intake: calorie_intake,
        calorie_burnt: calorie_burnt
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
      <div class="row"> Calories Intake: {response["calorie_intake"]}</div>
      <div class="row">Calories Burnt: {response["calorie_burnt"]}</div>
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