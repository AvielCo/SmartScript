import React, { useEffect } from 'react';
import { getAccessToken } from '../../helpers';
import { useHistory } from 'react-router-dom';

function Logout() {
  const history = useHistory();
  useEffect(() => {
    const accessToken = getAccessToken();

    if (!accessToken) {
      history.replace('/');
      return;
    }
    window.localStorage.removeItem('accessToken');
    window.sessionStorage.removeItem('accessToken');
    window.dispatchEvent(new Event('storage'));

    history.replace('/');
  }, []);
  return <div></div>;
}

export default Logout;
