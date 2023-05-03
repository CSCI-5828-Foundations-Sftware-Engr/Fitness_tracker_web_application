import { useNavigate } from "react-router-dom";
import logo from "./logo-transparent-svg.svg";
import React, { useState } from "react";

const LoginForm = props => {
    const [activeTab, setActiveTab] = useState('login');
    const [formData, setFormData] = useState({});
    const navigate = useNavigate();

    const handleTabChange = tab => {
        setActiveTab(tab);
    };

    const handleChange = event => {
        setFormData({ ...formData, [event.target.name]: event.target.value });
    };

    const handleSubmit = async event => {
        event.preventDefault();
        try {
            const response = await fetch(`https://fitness-tracker-staging.herokuapp.com/${activeTab.toLowerCase()}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(formData)
            });
            const data = await response.json();
            if (data.message === "Password matched") {
                navigate('dashboard', {
                    state: {
                        ...formData
                    }
                });
            }
            else {
                alert("Invalid username or password");
            }
        } catch (error) {
            console.error(error);
        }
    };

    return (
        <div id="loginform">
            <FormHeader activeTab={activeTab} handleTabChange={handleTabChange} />
            {activeTab === 'login' ? <LoginFormInput onChange={handleChange} handleSubmit={handleSubmit} /> : <SignupFormInput onChange={handleChange} handleSubmit={handleSubmit} />}
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
        <FormInput name="username" description="Username" placeholder="Enter Username" type="text" onChange={props.onChange} />
        <FormInput name="password" description="Password" placeholder="Enter Password" type="password" onChange={props.onChange} />
        <FormButton title="Submit" handleSubmit={props.handleSubmit} />
    </div>
);

const SignupFormInput = props => (
    <div>
        <FormInput name="username" description="Username" placeholder="Enter Username" type="text" onChange={props.onChange} />
        <FormInput name="password" description="Password" placeholder="Enter Password" type="password" onChange={props.onChange} />
        <FormInput name="email" description="Email" placeholder="Enter Email" type="email" onChange={props.onChange} />
        <FormInput name="contactNumber" description="Contact Number" placeholder="Enter Contact Number" type="number" onChange={props.onChange} />
        <FormButton title="Register" handleSubmit={props.handleSubmit} />
    </div>
);


const FormButton = props => {


    return (
        <div>
            <form onSubmit={props.handleSubmit}>
                <div id="button" className="row">
                    <button>{props.title}</button>
                </div>
            </form>
        </div>
    );
};

const FormInput = props => (
    <div className="row">
        <label>{props.description}</label>
        <input type={props.type} name={props.name} placeholder={props.placeholder} onChange={props.onChange} />
    </div>
);

export default LoginForm;