import './App.css';

function App() {
  return (
    <div class="mainPage">
      <LoginForm />
    </div>
  );
}

const LoginForm = props => (
  <div id="loginform">
    <FormHeader title="Login" />
    <Form />
  </div>
);

const FormHeader = props => (
  <h2 id="headerTitle">{props.title}</h2>
);


const Form = props => (
  <div>
    <FormInput description="Username" placeholder="Enter username" type="text" />
    <FormInput description="Password" placeholder="Enter password" type="password" />
    <FormButton title="Log in" />
  </div>
);

const FormButton = props => (
  <div id="button" class="row">
    <button>{props.title}</button>
  </div>
);

const FormInput = props => (
  <div class="row">
    <label>{props.description}</label>
    <input type={props.type} placeholder={props.placeholder} />
  </div>
);

export default App;
