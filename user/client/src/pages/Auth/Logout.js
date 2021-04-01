import React, { useEffect } from 'react';
import axios from 'axios';
import { getAccessToken } from '../../helpers';
import { useHistory } from 'react-router-dom';

function Logout() {
  const history = useHistory();
  const logout = () => {
    const accessToken = getAccessToken();
    if (!accessToken) {
      history.replace('/404');
    }
    const cfg = {
      headers: {
        Authorization: 'Bearer ' + accessToken,
      },
    };

    axios
      .delete('http://localhost:8008/api/auth/logout', cfg)
      .then((res) => {
        console.log(res);
        if (res.status === 204) {
          window.localStorage.removeItem('accessToken');
          window.sessionStorage.removeItem('accessToken');
          history.replace('/');
        }
      })
      .catch((err) => {
        console.log(err);
      });
  };

  useEffect(() => {
    logout();
  }, []);

  return <div></div>;
}

export default Logout;
