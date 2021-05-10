import "./App.css";
import React, { useEffect, useState } from "react";
import { toast, ToastContainer } from "react-toastify";
import { Home, Login, Register, Profile, Error, About } from "./pages";
import { NavBar } from "./components";
import { Switch, Route, useHistory } from "react-router-dom";
import { getAccessToken, removeAccessToken } from "./helpers";
import axios from "axios";
import "antd/dist/antd.css";

function App() {
  const [isUserLoggedIn, setIsUserLoggedIn] = useState(false);
  const [isUserBanned, setUserIsBanned] = useState(false);
  const history = useHistory();

  useEffect(() => {
    checkIfLoggedIn();
    window.addEventListener("storage", (ev) => {
      ev.preventDefault();
      checkIfLoggedIn();
    });
    return () => {
      window.removeEventListener("storage", (ev) => {
        ev.preventDefault();
        checkIfLoggedIn();
      });
    };
  }, []);

  const checkIfLoggedIn = () => {
    const cfg = {
      headers: {
        Authorization: "Bearer " + getAccessToken(),
      },
    };

    axios
      .get(`${process.env.REACT_APP_API_ADDRESS}/api/auth/`, cfg)
      .then((res) => {
        if (res.status === 200) {
          setUserIsBanned(false);
          setIsUserLoggedIn(true);
        }
      })
      .catch((err) => {
        if (err.response) {
          const { status } = err.response;
          if (status === 403) {
            removeAccessToken();
            setUserIsBanned(true);
            setIsUserLoggedIn(false);
            toast.error("Contact admin to submit ban appeal.");
            toast.error("You are banned.");
            history.replace("/ban");
            return;
          }
        }
      });
  };

  return (
    <>
      <NavBar isLoggedIn={isUserLoggedIn} setIsLoggedIn={setIsUserLoggedIn} />
      <ToastContainer position="top-left" autoClose={5000} hideProgressBar={false} newestOnTop closeOnClick rtl={false} pauseOnFocusLoss draggable pauseOnHover />
      <Switch>
        <Route exact path="/home">
          <Home isLoggedIn={isUserLoggedIn} />
        </Route>
        <Route exact path="/login">
          <Login setIsLoggedIn={setIsUserLoggedIn} />
        </Route>
        <Route exact path="/profile">
          <Profile isLoggedIn={isUserLoggedIn} />
        </Route>
        <Route exact path="/about">
          <About />
        </Route>
        <Route exact path="/register" component={Register} />
        <Route exact path="/">
          <Home isLoggedIn={isUserLoggedIn} />
        </Route>
        <Route component={Error} />
      </Switch>
    </>
  );
}
export default App;
