import React, { useState } from "react";
import axios from "axios";
import CryptoJS from "crypto-js";

function Login() {
  const handleSubmit = (event) => {
    event.preventDefault();
    const encryptedPassword = CryptoJS.AES.encrypt(
      JSON.stringify(event.target[1].value),
      process.env.REACT_APP_SECRET_KEY
    ).toString();
    const encryptedUsername = CryptoJS.AES.encrypt(
      JSON.stringify(event.target[0].value),
      process.env.REACT_APP_SECRET_KEY
    ).toString();
    loginUser(encryptedUsername, encryptedPassword);
  };

  const loginUser = (username, password) => {
    axios
      .post("http://localhost:8008/api/auth/login", null, {
        params: { username, password },
      })
      .then((response) => {
        console.log(response);
      })
      .catch((error) => {
        console.log(error);
      });
  };

  return (
    <React.Fragment>
      <form onSubmit={handleSubmit}>
        <label for='username'>
          <b>Username</b>
        </label>
        <input
          type='text'
          placeholder='Username'
          name='username'
          id='username'
          required
        />

        <label for='psw'>
          <b>Password</b>
        </label>
        <input
          type='password'
          placeholder='Enter Password'
          name='psw'
          id='psw'
          required
        />
        <button type='submit' className='registerbtn'>
          Register
        </button>
      </form>
    </React.Fragment>
  );
}

export default Login;