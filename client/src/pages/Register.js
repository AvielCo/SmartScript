import React, { useState } from 'react';
import axios from 'axios';

function Register() {
  const handleSubmit = (event) => {
    event.preventDefault();
    registerUser(event.target[0].value, event.target[1].value, event.target[2].value, event.target[3].value);
  };

  const registerUser = (email, username, password, name) => {
    axios
      .post('http://localhost:8008/api/auth/register', { email, username, password, name })
      .then(function (response) {
        console.log(response.data);
      })
      .catch(function (error) {
        console.log(error);
        //if(error.username || error.email) username or email already exists.
      });
  };

  return (
    <React.Fragment>
      <form onSubmit={handleSubmit}>
        <input type="text" placeholder="Enter Email" name="email" id="email" required />
        <input type="text" placeholder="Username" name="username" id="username" required />
        <input type="password" placeholder="Enter Password" name="psw" id="psw" required />
        <input type="text" placeholder="Name" name="name" id="name" required />
        <button type="submit" className="registerbtn">
          Register
        </button>
      </form>
    </React.Fragment>
  );
}

export default Register;
