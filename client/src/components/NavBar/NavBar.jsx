import React from 'react';
import { BrowserRouter } from 'react-router-dom';

import { AppBar } from '@material-ui/core';
import NavButton from '../Buttons/NavButton';
import logo from '../../assets/smartscript-logo.png';
import { BrowserRouter as Router, Link } from 'react-router-dom';
import './NavBar.css';
import Login from '../../pages/Auth/Login';

function NavBar({ isLoggedIn }) {
  const login = () => {
    return (
      <Router path="/login">
        <Login />
      </Router>
    );
  };

  return (
    <AppBar className="navbar" position="sticky">
      <div className="navbar-holder">
        <Link to="/home">
          <img alt="SmartScript-logo" src={logo} />
        </Link>
        <div className="btnGroup">
          <NavButton btnText="Scan" />
          <NavButton btnText="About" />
          <NavButton btnText="Who we are" />
          {!isLoggedIn && (
            <Link to="/login" style={{ textDecoration: 'none' }}>
              <NavButton btnText="Login" />
            </Link>
          )}
          {!isLoggedIn && (
            <Link to="/register" style={{ textDecoration: 'none' }}>
              <NavButton btnText="Register" />
            </Link>
          )}
          {isLoggedIn && (
            <Link to="/logout" style={{ textDecoration: 'none' }}>
              <NavButton btnText="Logout" />
            </Link>
          )}
        </div>
        <div className="burger" id="burger">
            <div class="line-1"></div>
            <div class="line-2"></div>
            <div class="line-3"></div>
        </div>
      </div>

    </AppBar>
  );
}

export default NavBar;
