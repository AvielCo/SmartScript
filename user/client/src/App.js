import "./App.css";
import React, { useEffect, useState } from "react";
import { Home, Login, Register, Profile, Error, Banned } from "./pages";
import { Switch, Route, useHistory, Redirect } from "react-router-dom";
import { getAccessToken } from "./helpers";
import axios from "axios";
import "antd/dist/antd.css";
import { HashLink } from "react-router-hash-link";

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [userIsBanned, setUserIsBanned] = useState(false);
  const history = useHistory();

  useEffect(() => {
    isBanned();
  }, [isLoggedIn]);

  const isBanned = () => {
    const cfg = {
      headers: {
        Authorization: "Bearer " + getAccessToken(),
      },
    };

    axios
      .get(`${process.env.REACT_APP_API_ADDRESS}/api/auth/user`, cfg)
      .then((res) => {
        if (res.status === 200) {
          setUserIsBanned(false);
          setIsLoggedIn(true);
        }
      })
      .catch((err) => {
        if (err.response) {
          const { status } = err.response;
          if (status === 403) {
            setUserIsBanned(true);
            setIsLoggedIn(false);
            history.replace("/ban");
            return;
          }
        }
      });
  };
  return (
    <Switch>
      <Route exact path="/ban" component={Banned} />
      <Route exact path="/home">
        <Home isLoggedIn={isLoggedIn} setIsLoggedIn={setIsLoggedIn} />
      </Route>
      <Route exact path="/login">
        <Login setIsLoggedIn={setIsLoggedIn} />
      </Route>
      <Route exact path="/profile" component={Profile} />
      <Route exact path="/register" component={Register} />
      <Route exact path="/">
        <Home isLoggedIn={isLoggedIn} setIsLoggedIn={setIsLoggedIn} />
      </Route>
      <Route component={Error} />
      {userIsBanned && <Redirect to="/ban" />}
    </Switch>
  );
}
export default App;
