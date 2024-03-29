import React, { useState } from "react";
import axios from "axios";
import { useHistory, Redirect } from "react-router-dom";
import { Form } from "antd";
import { UserOutlined, LockOutlined, MailOutlined, KeyOutlined } from "@ant-design/icons";
import { toast } from "react-toastify";
import InputField from "../../components/InputField/InputField";
import InputButton from "../../components/Buttons/InputButton";
import { encryptStrings, getAccessToken } from "../../helpers";

import "react-toastify/dist/ReactToastify.css";
import "./Auth.css";

function Register() {
  const [inputUsername, setUsername] = useState("");
  const [inputPassword, setPassword] = useState("");
  const [inputEmail, setEmail] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const history = useHistory();

  const handleSubmit = (event) => {
    event.preventDefault();
    if (isLoading) {
      toast.info("Please wait.");
      return;
    }
    if (!inputUsername || !inputPassword || !inputEmail) {
      toast.info("Some fields are empty.");
      return;
    }
    setIsLoading(true);
    const { encryptedUsername, encryptedPassword, encryptedEmail } = encryptStrings({ encryptedUsername: inputUsername }, { encryptedPassword: inputPassword }, { encryptedEmail: inputEmail });

    registerUser(encryptedEmail, encryptedUsername, encryptedPassword);
  };

  const registerUser = (email, username, password, name) => {
    axios
      .post(`${process.env.REACT_APP_API_ADDRESS}/api/auth/register`, {
        email,
        username,
        password,
      })
      .then(function (response) {
        setIsLoading(false);
        if (response.status === 200) {
          toast.info(`Please log in with your username and password!`);
          toast.info(`Welcome to SmartScript!`);
          history.replace("/login");
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
        <form onSubmit={handleSubmit} className="auth">
          <div className="form">
            <h3>Register</h3>
            <div className="inputfields">
              <Form.Item name="email" label="Email" rules={[{ required: true, message: "Please enter your email." }]}>
                <InputField type="text" value="email" name="email" setProperty={setEmail} prefix={<MailOutlined />} />
              </Form.Item>

              <Form.Item name="username" label="Username" rules={[{ required: true, message: "Please enter a valid username." }]}>
                <InputField type="text" value="username" name="username" setProperty={setUsername} prefix={<LockOutlined />} />
              </Form.Item>

              <Form.Item
                name="password"
                label="Password"
                rules={[
                  { required: true, message: "Please enter a valid password." },
                  { type: "email", message: "The input is not valid E-mail!" },
                ]}>
                <InputField type="password" value="password" name="password" setProperty={setPassword} prefix={<KeyOutlined />} />
              </Form.Item>

              <InputButton name="Register" type="submit" />
            </div>
          </div>
        </form>
      )}
    </React.Fragment>
  );
}

export default Register;
