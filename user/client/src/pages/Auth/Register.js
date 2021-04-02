import React, { useState } from 'react';
import axios from 'axios';

import { Form } from 'antd';
import { UserOutlined, LockOutlined, MailOutlined, KeyOutlined } from '@ant-design/icons';

import InputField from '../../components/InputField/InputField';
import InputButton from '../../components/Buttons/InputButton';
import NavBar from '../../components/NavBar/NavBar';
import { encryptStrings } from '../../helpers';

import './Register.css';

function Register() {
  const [inputUsername, setUsername] = useState('');
  const [inputPassword, setPassword] = useState('');
  const [inputEmail, setEmail] = useState('');
  const [inputName, setName] = useState('');

  const handleSubmit = (event) => {
    event.preventDefault();
    if (!inputUsername || !inputPassword) {
      return;
    }
    const { encryptedUsername, encryptedPassword, encryptedEmail, encryptedName } = encryptStrings(
      { encryptedUsername: inputUsername },
      { encryptedPassword: inputPassword },
      { encryptedEmail: inputEmail },
      { encryptedName: inputName }
    );

    registerUser(encryptedEmail, encryptedUsername, encryptedPassword, encryptedName);
  };

  const registerUser = (email, username, password, name) => {
    axios
      .post('http://localhost:8008/api/auth/register', {
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

  useEffect(() => {
    const accessToken = getAccessToken();
    if (accessToken) {
      // redirect to home
    }
  });

  return (
    <React.Fragment>
      <NavBar />
      <Form onFinish={handleSubmit} className="register-page">
        <div className="register-form">
          <h3>Register</h3>
          <div className="register-inputfields">
            <Form.Item name="Email" label="Email" rules={[{ required: true, message: 'Please enter you email.' }]}>
              <InputField type="text" setProperty={setEmail} prefix={<MailOutlined />} />
            </Form.Item>
            <Form.Item name="username" label="Username" rules={[{ required: true, message: 'Please enter a valid username.' }]}>
              <InputField type="text" setProperty={setUsername} prefix={<LockOutlined />} />
            </Form.Item>
            <Form.Item
              name="Password"
              label="Password"
              rules={[
                { required: true, message: 'Please enter a valid password.' },
                { type: 'email', message: 'The input is not valid E-mail!' },
              ]}>
              <InputField type="password" setProperty={setPassword} prefix={<KeyOutlined />} />
            </Form.Item>
            <Form.Item name="Name" label="Name" rules={[{ required: true, message: 'Please enter a valid name.' }]}>
              <InputField type="text" setProperty={setName} prefix={<UserOutlined />} />
            </Form.Item>
            <InputButton name="Register" type="submit" />
          </div>
        </div>
      </Form>
    </React.Fragment>
  );
}

export default Register;
