import React, { useState, useEffect } from 'react';
import { useHistory } from 'react-router-dom';
import axios from 'axios';
import './Login.css';
import InputButton from '../components/Buttons/InputButton';
import InputField from '../components/InputField/InputField';
import NavBar from '../components/NavBar/NavBar';
import { encryptStrings, getAccessToken } from '../helpers';

import './Login.css';

function Login() {
  const [inputUsername, setUsername] = useState('');
  const [inputPassword, setPassword] = useState('');
  const history = useHistory();
  const handleSubmit = (event) => {
    event.preventDefault();
    console.log('login');
    if (!inputUsername || !inputPassword) {
      return;
    }
    const { encryptedUsername, encryptedPassword } = encryptStrings({ encryptedUsername: inputUsername }, { encryptedPassword: inputPassword });
    loginUser(encryptedUsername, encryptedPassword);
  };

  const loginUser = (username, password) => {
    axios
      .post('http://localhost:8008/api/auth/login', { username, password })
      .then((response) => {
        if (response.status === 200) {
          window.sessionStorage.setItem('accessToken', response.data.accessToken);
          history.push('/');
          return;
        }
        //TODO: show error that en error has been occurred
        return;
      })
      .catch((error) => {
        console.log(error);
      });
  };

  useEffect(() => {
    const accessToken = getAccessToken();
    if (accessToken) {
      // redirect to home
    }
  });

  return (
    <React.Fragment>
      <NavBar />
      <form onSubmit={handleSubmit} className="login">
        <div className="login-container">
          <h3>Login</h3>

          <div className="login-holder">
            <InputField value="username" type="text" name="username" setProperty={setUsername} />
            <InputField value="password" type="password" name="password" setProperty={setPassword} />
            <InputButton name="Login" type="submit"></InputButton>
          </div>
        </div>
      </form>
    </React.Fragment>
  );
}

export default Login;
