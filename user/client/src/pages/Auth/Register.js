import React, { useState } from 'react';
import axios from 'axios';
import { useHistory, Redirect } from 'react-router-dom';
import { Form, Row } from 'antd';
import { UserOutlined, LockOutlined, MailOutlined, KeyOutlined } from '@ant-design/icons';
import { ToastContainer, toast } from 'react-toastify';
import InputField from '../../components/InputField/InputField';
import InputButton from '../../components/Buttons/InputButton';
import NavBar from '../../components/NavBar/NavBar';
import { encryptStrings, getAccessToken } from '../../helpers';

import 'react-toastify/dist/ReactToastify.css';
import './Register.css';

function Register() {
  const [inputUsername, setUsername] = useState('');
  const [inputPassword, setPassword] = useState('');
  const [inputEmail, setEmail] = useState('');
  const [inputName, setName] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const history = useHistory();

  const handleSubmit = (event) => {
    event.preventDefault();
    if (isLoading) {
      toast.info('Please wait.');
      return;
    }
    if (!inputUsername || !inputPassword || !inputEmail || !inputName) {
      toast.info('Some fields are empty.');
      return;
    }
    setIsLoading(true);
    const { encryptedUsername, encryptedPassword, encryptedEmail, encryptedName } = encryptStrings(
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
      .post(`http://${process.env.REACT_APP_API_ADDRESS}:8008/api/auth/register`, {
        email,
        username,
        password,
        name,
      })
      .then(function (response) {
        setIsLoading(false);
        if (response.status === 200) {
          window.sessionStorage.setItem(
            "accessToken",
            response.data.accessToken
          );
          history.replace("/");
          window.dispatchEvent(new Event("storage"));
          return;
        }
      })
      .catch((err) => {
        setIsLoading(false);
        if (err.response) {
          const { status, message } = err.response.data.error;
          if (status === 404) {
            history.replace("/404");
            return;
          }
          toast(message);
        }
      });
  };

  return (
    <React.Fragment>
      {getAccessToken() ? (
        <Redirect to="/home" />
      ) : (
        <>
          <ToastContainer position="top-left" autoClose={5000} hideProgressBar={false} newestOnTop closeOnClick rtl={false} pauseOnFocusLoss draggable pauseOnHover />
          <NavBar />
          <form onSubmit={handleSubmit} className="register-page">
            <div className="register-form">
              <h3>Register</h3>
              <div className="register-inputfields">
                <Row>
                  <Form.Item name="email" label="email" rules={[{ required: true, message: 'Please enter your email.' }]}>
                    <InputField type="text" value="email" name="email" setProperty={setEmail} prefix={<MailOutlined />} />
                  </Form.Item>
                </Row>
                <Row>
                  <Form.Item name="username" label="username" rules={[{ required: true, message: 'Please enter a valid username.' }]}>
                    <InputField type="text" value="username" name="username" setProperty={setUsername} prefix={<LockOutlined />} />
                  </Form.Item>
                </Row>
                <Row>
                  <Form.Item
                    name="password"
                    label="password"
                    rules={[
                      { required: true, message: 'Please enter a valid password.' },
                      { type: 'email', message: 'The input is not valid E-mail!' },
                    ]}>
                    <InputField type="password" value="password" name="password" setProperty={setPassword} prefix={<KeyOutlined />} />
                  </Form.Item>
                </Row>
                <Row>
                  <Form.Item name="name" label="Name" rules={[{ required: true, message: 'Please enter a valid name.' }]}>
                    <InputField type="text" value="name" name="name" setProperty={setName} prefix={<UserOutlined />} />
                  </Form.Item>
                </Row>
                <InputButton name="Register" type="submit" />
              </div>
            </div>
          </form>
        </>
      )}
    </React.Fragment>
  );
}

export default Register;
