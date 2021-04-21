import React, { useState, useEffect } from 'react';
import { Redirect, useHistory } from 'react-router-dom';
import axios from 'axios';
import './Login.css';
import { Checkbox, Form } from 'antd';
import { InputButton, InputField } from '../../components';
import { encryptStrings, getAccessToken } from '../../helpers';
import { UserOutlined, LockOutlined } from '@ant-design/icons';
import { ToastContainer, toast } from 'react-toastify';
import './Login.css';

function Login() {
  const [form] = Form.useForm();

  const [inputUsername, setUsername] = useState('');
  const [inputPassword, setPassword] = useState('');
  const [checked, setChecked] = useState(false);
  const history = useHistory();

  const handleSubmit = (event) => {
    event.preventDefault();
    if (!inputUsername || !inputPassword) {
      return;
    }
    const { encryptedUsername, encryptedPassword } = encryptStrings({ encryptedUsername: inputUsername }, { encryptedPassword: inputPassword });

    loginUser(encryptedUsername, encryptedPassword);
  };

  const loginUser = (username, password) => {
    axios
      .post(`http://${process.env.REACT_APP_API_ADDRESS}:8080/api/auth/login`, { username, password })
      .then((response) => {
        if (response.status === 200) {
          window.sessionStorage.setItem('accessToken', response.data.accessToken);
          if (checked) {
            window.localStorage.setItem('accessToken', response.data.accessToken);
          }
        }
      })
      .catch((err) => {
        if (err.response) {
          const { status, message } = err.response.data.error;
          if (status === 404) {
            history.replace('/404');
            return;
          }
          toast.error(message);
        }
      })
      .finally(() => history.replace('/'));
  };

  //garachia kartoshta
  return (
    <React.Fragment>
      {getAccessToken() ? (
        <Redirect to="/home" />
      ) : (
        <>
          <ToastContainer position="top-left" autoClose={5000} hideProgressBar={false} newestOnTop closeOnClick rtl={false} pauseOnFocusLoss draggable pauseOnHover />
          <form onSubmit={handleSubmit} className="login">
            <div className="login-container">
              <h3>Login</h3>
              <div className="login-holder">
                <Form.Item
                  name="username"
                  label="Username"
                  rules={[
                    { required: true, message: 'Please enter your username.' },
                    { type: 'text', message: 'Please enter a valid username.' },
                  ]}>
                  <InputField value="username" type="text" name="username" setProperty={setUsername} prefix={<UserOutlined />} />
                </Form.Item>
                <Form.Item name="password" label="Password" rules={[{ required: true, message: 'Please input your Password!' }]}>
                  <InputField value="password" type="password" name="password" setProperty={setPassword} prefix={<LockOutlined />} />
                </Form.Item>
                <Checkbox checked={checked} onChange={(e) => setChecked(e.target.checked)}>
                  Remember me
                </Checkbox>
                <InputButton name="Login" type="submit" />
              </div>
            </div>
          </form>
        </>
      )}
    </React.Fragment>
  );
}

export default Login;
