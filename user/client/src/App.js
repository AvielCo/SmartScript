import './App.css';
import React, { useEffect, useState } from 'react';
import { Home, Login, Register, Profile, Error, Logout, Banned } from './pages';
import { Switch, Route, useHistory, Redirect } from 'react-router-dom';
import { getAccessToken } from './helpers';
import axios from 'axios';
import 'antd/dist/antd.css';

function App() {
  const [token, setToken] = useState(getAccessToken());
  const [userIsBanned, setuserIsBanned] = useState(false);
  const history = useHistory();

  useEffect(() => {
    isBanned();
    window.addEventListener('storage', (ev) => {
      isBanned();
    });
    return () => {
      window.removeEventListener('storage', (ev) => {});
    };
  }, []);

  const isBanned = () => {
    const accessToken = getAccessToken();

    const cfg = {
      headers: {
        Authorization: 'Bearer ' + accessToken,
      },
    };
    axios
      .get(`http://${process.env.REACT_APP_API_ADDRESS}:8008/api/auth/user`, cfg)
      .then((res) => {
        setuserIsBanned(false);
        setToken(accessToken);
      })
      .catch((err) => {
        if (err.response) {
          const { status } = err.response;
          if (status === 403) {
            setuserIsBanned(true);
            history.replace('/ban');
            return;
          }
        }
      });
  };

  return (
    <Switch>
      <Route exact path="/ban" component={Banned} />
      <Route exact path="/home" component={Home} />
      <Route exact path="/login" component={Login} />
      <Route exact path="/logout" component={Logout} />
      <Route exact path="/profile" component={Profile} />
      <Route exact path="/register" component={Register} />
      <Route exact path="/" component={Home} />
      <Route component={Error} />
      {userIsBanned && <Redirect to="/ban" />}
    </Switch>
  );
}
export default App;
