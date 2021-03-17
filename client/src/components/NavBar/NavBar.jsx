import React from 'react';
import { AppBar } from '@material-ui/core';
import NavButton from '../Buttons/NavButton';
import logo from '../../assets/smartscript-logo.png';
import {
  BrowserRouter as Router,Link
} from "react-router-dom";
import './NavBar.css';
import Login from '../../pages/Login';


function NavBar() {

  const login=()=>{
    return(
      <Router path="/login">
        <Login />
      </Router>
    )
  }

  return (
      <AppBar position="sticky">
        <div className="navbar-holder">
          <img alt="SmartScript-logo" src={logo} />
          <div className="btnGroup">
            <NavButton btnText="Scan" />
            <NavButton btnText="About" />
            <NavButton btnText="Who we are" />
            <Link to="/login">Login</Link>
          </div>
        </div>
      </AppBar>
  );
}

export default NavBar;
