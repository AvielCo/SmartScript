import React, { useState } from "react";
import { useHistory, Redirect } from "react-router-dom";
import axios from "axios";
import { toast } from "react-toastify";
import { Checkbox, Form } from "antd";
import { InputButton, InputField } from "../../components";
import { encryptStrings } from "../../helpers";
import { UserOutlined, LockOutlined } from "@ant-design/icons";
import { getAccessToken } from "../../helpers";

import "react-toastify/dist/ReactToastify.css";
import "./Auth.css";

function Login({ setIsLoggedIn }) {
  const [inputUsername, setUsername] = useState("");
  const [inputPassword, setPassword] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const history = useHistory();
  const [checked, setChecked] = useState(false);

  const handleSubmit = (event) => {
    event.preventDefault();
    if (isLoading) {
      toast.info("Please wait.");
      return;
    }
    if (!inputUsername || !inputPassword) {
      toast.info("Username and password are required.");
      return;
    }
    setIsLoading(true);
    const { encryptedUsername, encryptedPassword } = encryptStrings({ encryptedUsername: inputUsername }, { encryptedPassword: inputPassword });

    loginUser(encryptedUsername, encryptedPassword);
  };

  const loginUser = (username, password) => {
    axios
      .post(`${process.env.REACT_APP_API_ADDRESS}/api/auth/login`, {
        username,
        password,
      })
      .then((response) => {
        setIsLoading(false);
        if (response.status === 200) {
          window.sessionStorage.setItem("accessToken", response.data.accessToken);
          if (checked) {
            window.localStorage.setItem("accessToken", response.data.accessToken);
          }
          setIsLoggedIn(true);
          toast.success(`Logged in successfully!`);
          history.replace("/");
          return;
        }
      })
      .catch((err) => {
        if (err.response) {
          const { status, message } = err.response.data.error;
          if (status === 404) {
            history.replace("/404");
          } else if (status === 401) {
            toast.error(message);
          } else if (status === 403) {
            toast.error("You are banned.");
            toast.error("Contact an admin to submit ban appeal.");
          } else toast.error("Internal Server Error.");
          setIsLoading(false);
        }
      });
  };
  //garachia kartoshta
  return (
    <React.Fragment>
      {getAccessToken() ? (
        <Redirect to="/home" />
      ) : (
        <form onSubmit={handleSubmit} className="auth">
          <div className="form">
            <h3>Login</h3>
            <div className="inputfields">
              <Form.Item
                name="username"
                label="Username"
                rules={[
                  { required: true, message: "Please enter your username." },
                  { type: "text", message: "Please enter a valid username." },
                ]}>
                <InputField value="username" type="text" name="username" setProperty={setUsername} prefix={<UserOutlined />} />
              </Form.Item>
              <Form.Item name="password" label="Password" rules={[{ required: true, message: "Please input your Password!" }]}>
                <InputField value="password" type="password" name="password" setProperty={setPassword} prefix={<LockOutlined />} />
              </Form.Item>
              <Checkbox className="check-box" checked={checked} onChange={(e) => setChecked(e.target.checked)}>
                Remember me
              </Checkbox>
              <InputButton name="Login" type="submit"></InputButton>
            </div>
          </div>
        </form>
      )}
    </React.Fragment>
  );
}

export default Login;
