import React from 'react';
import axios from 'axios';
import './Login.css';
import InputButton from "../components/Buttons/InputButton";
import InputField from "../components/InputField/InputField";

function Login() {
  const handleSubmit = (event) => {
    event.preventDefault();
    loginUser(event.target[0].value, event.target[1].value);
  };

  const loginUser = (username, password) => {
    axios
      .post('http://localhost:8008/api/auth/login', null, { params: { username, password } })
      .then((response) => {
        console.log(response);
      })
      .catch((error) => {
        console.log(error);
      });
  };

  return (
    <React.Fragment>
      <form onSubmit={handleSubmit} className="login">
        <div className="login-container">
          <h3>LOGIN</h3>
          <div className="login-holder">
            <InputField name="username"/>
            <InputField name="password"/>
            <InputButton name="LOGIN"></InputButton>
          </div>
        </div>
      </form>
    </React.Fragment>
  );
}

export default Login;
