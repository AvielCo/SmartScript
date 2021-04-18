import "./App.css";
import React, { useEffect, useState } from "react";
import { Home, Login, Register, Profile, Error, Logout, Banned } from "./pages";
import {
  BrowserRouter as Router,
  Switch,
  Route,
  useHistory,
} from "react-router-dom";
import { getAccessToken } from "./helpers";
import axios from "axios";
import "antd/dist/antd.css";

function App() {
  const [token, setToken] = useState(getAccessToken());
  const history = useHistory();

  useEffect(() => {
    isBanned();
    window.addEventListener("storage", (ev) => {
      isBanned();
    });
    return () => {
      window.removeEventListener("storage", (ev) => {});
    };
  }, []);

  const isBanned = () => {
    let accessToken = getAccessToken();

    const cfg = {
      headers: {
        Authorization: "Bearer " + accessToken,
      },
    };
    axios
      .get("http://${process.env.REACT_APP_API_ADDRESS}:8008/api/auth/user", cfg)
      .then((res) => {
        setToken(accessToken);
      })
      .catch((err) => {
        if (err.response) {
          const { status } = err.response;
          if (status === 403) {
            history.push("/ban");
            return;
          }
        }
      });
  };

  return (
    <Switch>
      <Route exact path="/profile" component={token ? Profile : Home} />
      <Route exact path="/register" component={token ? Home : Register} />
      <Route exact path="/login" component={token ? Home : Login} />
      <Route exact path="/home" component={Home} />
      <Route exact path="/logout" component={token ? Logout : Home} />
      <Route exact path="/ban" component={Banned} />
      <Route exact path="/" component={Home} />
      <Route component={Error} />
    </Switch>
  );
}
export default App;
