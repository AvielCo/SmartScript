import React from 'react';
import { BrowserRouter} from "react-router-dom";

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
        <Link to="/home"><img alt="SmartScript-logo" src={logo} /></Link>
          <div className="btnGroup">
            <NavButton btnText="Scan" />
            <NavButton btnText="About" />
            <NavButton btnText="Who we are" />
            <Link to="/login" style={{ textDecoration: 'none' }}><NavButton btnText="Login" /></Link>
            <Link to="/register" style={{ textDecoration: 'none' }}><NavButton btnText="Register"/></Link>
          </div>
        </div>
      </AppBar>
  );
}

export default NavBar;
