import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useHistory } from 'react-router-dom';
import { Form } from 'antd';
import { UserOutlined, LockOutlined, MailOutlined, KeyOutlined } from '@ant-design/icons';

import InputField from '../../components/InputField/InputField';
import InputButton from '../../components/Buttons/InputButton';
import NavBar from '../../components/NavBar/NavBar';
import { encryptStrings, getAccessToken } from '../../helpers';

import './Register.css';

function Register() {
  const [inputUsername, setUsername] = useState('');
  const [inputPassword, setPassword] = useState('');
  const [inputEmail, setEmail] = useState('');
  const [inputName, setName] = useState('');
  const history = useHistory();
  const [form] = Form.useForm();

  const handleSubmit = (event) => {
    event.preventDefault();
    if (!inputUsername || !inputPassword || !inputEmail || !inputName) {
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
      .post('/api/auth/register', {
        email,
        username,
        password,
        name,
      })
      .then(function (response) {
        if (response.status === 200) {
          window.sessionStorage.setItem('accessToken', response.data.accessToken);
          history.replace('/');
          window.dispatchEvent(new Event('storage'));
          return;
        }
      })
      .catch((err) => {
        if (err.response) {
          const { status, message } = err.response.data.error;
          if (status === 404) {
            history.replace('/404');
            return;
          }
          alert(message);
        } else {
          alert('Internal Server Error');
        }
      });
  };

  return (
    <React.Fragment>
      <NavBar />
      <form onSubmit={handleSubmit} className="register-page">
        <div className="register-form">
          <h3>Register</h3>
          <div className="register-inputfields">
            <Form.Item name="email" label="Email" rules={[{ required: true, message: 'Please enter your email.' }]}>
              <InputField type="text" value="email" name="email" setProperty={setEmail} prefix={<MailOutlined />} />
            </Form.Item>
            <Form.Item name="username" label="Username" rules={[{ required: true, message: 'Please enter a valid username.' }]}>
              <InputField type="text" value="username" name="username" setProperty={setUsername} prefix={<LockOutlined />} />
            </Form.Item>
            <Form.Item
              name="password"
              label="Password"
              rules={[
                { required: true, message: 'Please enter a valid password.' },
                { type: 'email', message: 'The input is not valid E-mail!' },
              ]}>
              <InputField type="password" value="password" name="password" setProperty={setPassword} prefix={<KeyOutlined />} />
            </Form.Item>
            <Form.Item name="name" label="Name" rules={[{ required: true, message: 'Please enter a valid name.' }]}>
              <InputField type="text" value="name" name="name" setProperty={setName} prefix={<UserOutlined />} />
            </Form.Item>
            <InputButton name="Register" type="submit" />
          </div>
        </div>
      </form>
    </React.Fragment>
  );
}

export default Register;
