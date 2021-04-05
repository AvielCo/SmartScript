import React, { useEffect } from 'react';
import { getAccessToken } from '../../helpers';
import { useHistory } from 'react-router-dom';

function Logout() {
  const history = useHistory();
  useEffect(() => {
    const accessToken = getAccessToken();

    if (!accessToken) {
      history.replace('/404');
      return;
    }
    window.localStorage.removeItem('accessToken');
    window.sessionStorage.removeItem('accessToken');
    history.replace('/');
  }, []);
  return <div></div>;
}

export default Logout;
