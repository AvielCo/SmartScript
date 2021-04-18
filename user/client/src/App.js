import "./App.css";
import React, { useEffect, useState } from "react";
import { Home, Login, Register, Profile, Error, Logout, Banned } from "./pages";
import { BrowserRouter as Router, Switch, Route } from "react-router-dom";
import { getAccessToken } from "./helpers";
import "antd/dist/antd.css";

function App() {
  const [token, setToken] = useState(getAccessToken());
  useEffect(() => {
    window.addEventListener("storage", (ev) => {
      setToken(getAccessToken());
    });
    return () => {
      window.removeEventListener("storage", (ev) => {});
    };
  }, []);

  return (
    <Router>
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
    </Router>
  );
}
export default App;
