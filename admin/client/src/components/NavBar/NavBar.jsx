import React, { useEffect } from 'react';
import NavButton from '../Buttons/NavButton';
import logo from '../../assets/smartscript-logo.png';
import axios from 'axios';
import { useState } from 'react';
import { Link } from 'react-router-dom';
import { getAccessToken } from '../../helpers';
import { useHistory } from 'react-router-dom';

import './NavBar.css';

function NavBar() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [slide, setSlide] = useState(0);
  const showSidebar = () => setSlide(!slide);
  const history = useHistory();

  const logout = () => {
    const accessToken = getAccessToken();

    if (!accessToken) {
      history.replace('/');
      return;
    }

    window.localStorage.removeItem('accessToken');
    window.sessionStorage.removeItem('accessToken');
    window.dispatchEvent(new Event('storage'));
    const cfg = {
      headers: {
        Authorization: 'Bearer ' + accessToken,
        isAdmin: true,
      },
    };

    axios
      .delete(`http://${process.env.REACT_APP_API_ADDRESS}:8080/api/auth/logout`, cfg)
      .then((res) => {
        if (res.status === 204) {
          setIsLoggedIn(false);
          history.replace('/');
        }
      })
      .catch((err) => {
        if (err.response) {
          const { status, message } = err.response.data.error;
          if (status === 404) {
            history.replace('/404');
            return;
          }
        }
      });
  };

  useEffect(() => {
    if (isLoggedIn) return;
    const cfg = {
      headers: {
        Authorization: 'Bearer ' + getAccessToken(),
        isAdmin: true,
      },
    };
    axios
      .get(`http://${process.env.REACT_APP_API_ADDRESS}:8080/api/auth/user`, cfg)
      .then((res) => {
        if (res.status === 200) {
          setIsLoggedIn(true);
        }
      })
      .catch((err) => {
        setIsLoggedIn(false);
      });
  }, [isLoggedIn]);

  return (
    <nav className="navbar" position="sticky">
      <Link className="logo" to="/home">
        <img alt="SmartScript-logo" src={logo} />
      </Link>
      <h3>Admin Panel</h3>
      <div className={slide ? 'navbar-holder active' : 'navbar-holder'} slide={slide}>
        {!isLoggedIn && (
          <Link to="/login" style={{ textDecoration: 'none' }}>
            <NavButton className="nav-button" btnText="Login" />
          </Link>
        )}
        {isLoggedIn && (
          <Link to="/home" style={{ textDecoration: 'none' }}>
            <NavButton className="nav-button" btnText="Logout" onClick={() => logout()} />
          </Link>
        )}
      </div>
      <div onClick={showSidebar} className={slide ? 'burger cross' : 'burger'} id="burger">
        <div className="line-1"></div>
        <div className="line-2"></div>
        <div className="line-3"></div>
      </div>
    </nav>
  );
}

export default NavBar;
