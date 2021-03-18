import React, { useState } from "react";
import axios from "axios";

import InputField from "../components/InputField/InputField";
import InputButton from "../components/Buttons/InputButton";
import NavBar from "../components/NavBar/NavBar";
import { encryptStrings } from "../helpers";

import "./Register.css";

function Register() {
  const [inputUsername, setUsername] = useState("");
  const [inputPassword, setPassword] = useState("");
  const [inputEmail, setEmail] = useState("");
  const [inputName, setName] = useState("");

  const handleSubmit = (event) => {
    event.preventDefault();
    if (!inputUsername || !inputPassword) {
      return;
    }
    const {
      encryptedUsername,
      encryptedPassword,
      encryptedEmail,
      encryptedName,
    } = encryptStrings(
      { encryptedUsername: inputUsername },
      { encryptedPassword: inputPassword },
      { encryptedEmail: inputEmail },
      { encryptedName: inputName }
    );

    registerUser(
      encryptedEmail,
      encryptedUsername,
      encryptedPassword,
      encryptedName
    );
  };

  const registerUser = (email, username, password, name) => {
    axios
      .post("http://localhost:8008/api/auth/register", {
        email,
        username,
        password,
        name,
      })
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
      <NavBar />
      <form className='register-page' onSubmit={handleSubmit}>
        <div className='register-form'>
          <h3>Register</h3>
          <div className='register-inputfields'>
            <InputField
              value='Email'
              type='text'
              name='Email'
              setProperty={setEmail}
            />
            <InputField
              value='Username'
              type='text'
              name='Username'
              setProperty={setUsername}
            />
            <InputField
              value='Password'
              type='text'
              name='Password'
              setProperty={setPassword}
            />
            <InputField
              value='Name'
              type='text'
              name='Name'
              setProperty={setName}
            />
            <InputButton name='Register'></InputButton>
          </div>
        </div>
      </form>
    </React.Fragment>
  );
}

export default Register;
