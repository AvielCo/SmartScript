import React, { useState } from "react";
import { useHistory } from "react-router-dom";
import axios from "axios";
import { ToastContainer, toast } from "react-toastify";
import "./Login.css";
import { Checkbox, Form } from "antd";
import { InputButton, InputField, NavBar } from "../../components";
import { encryptStrings } from "../../helpers";
import { UserOutlined, LockOutlined } from "@ant-design/icons";

import "react-toastify/dist/ReactToastify.css";
import "./Login.css";

function Login() {
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
    const { encryptedUsername, encryptedPassword } = encryptStrings(
      { encryptedUsername: inputUsername },
      { encryptedPassword: inputPassword }
    );

    loginUser(encryptedUsername, encryptedPassword);
  };

  const loginUser = (username, password) => {
    axios
      .post(`http://${process.env.REACT_APP_API_ADDRESS}:8008/api/auth/login`, {
        username,
        password,
      })
      .then((response) => {
        setIsLoading(false);
        if (response.status === 200) {
          window.sessionStorage.setItem(
            "accessToken",
            response.data.accessToken
          );
          if (checked) {
            window.localStorage.setItem(
              "accessToken",
              response.data.accessToken
            );
          }
          history.replace("/");
          window.dispatchEvent("storage");
          return;
        }
        return;
      })
      .catch((err) => {
        if (err.response) {
          const { status, message } = err.response.data.error;
          if (status === 404) {
            history.replace("/404");
          } else if (status === 401) {
            toast.error(message);
          } else toast.error("Internal Server Error.");
          setIsLoading(false);
        }
      });
  };
  //garachia kartoshta
  return (
    <React.Fragment>
      <ToastContainer
        position="top-left"
        autoClose={5000}
        hideProgressBar={false}
        newestOnTop
        closeOnClick
        rtl={false}
        pauseOnFocusLoss
        draggable
        pauseOnHover
      />
      <NavBar />
      <form onSubmit={handleSubmit} className="login">
        <div className="login-container">
          <h3>Login</h3>
          <div className="login-holder">
            <Form.Item
              name="username"
              label="Username"
              rules={[
                { required: true, message: "Please enter your username." },
                { type: "text", message: "Please enter a valid username." },
              ]}
            >
              <InputField
                value="username"
                type="text"
                name="username"
                setProperty={setUsername}
                prefix={<UserOutlined />}
              />
            </Form.Item>
            <Form.Item
              name="password"
              label="Password"
              rules={[
                { required: true, message: "Please input your Password!" },
              ]}
            >
              <InputField
                value="password"
                type="password"
                name="password"
                setProperty={setPassword}
                prefix={<LockOutlined />}
              />
            </Form.Item>
            <Checkbox
              className="check-box"
              checked={checked}
              onChange={(e) => setChecked(e.target.checked)}
            >
              Remember me
            </Checkbox>
            <InputButton
              name="Login"
              type="submit"
              disabled={isLoading}
            ></InputButton>
          </div>
        </div>
      </form>
    </React.Fragment>
  );
}

export default Login;
