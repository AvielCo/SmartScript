import React from 'react';
import { AppBar } from '@material-ui/core';
import NavButton from '../Buttons/NavButton';
import logo from '../../assets/smartscript-logo.png';
import './NavBar.css';

function NavBar() {
  return (
    <AppBar position="sticky">
      <div className="navbar-holder">
        <img alt="SmartScript-logo" src={logo} />
        <div className="btnGroup">
          <NavButton btnText="Scan" />
          <NavButton btnText="About" />
          <NavButton btnText="Who we are" />
        </div>
      </div>
    </AppBar>
  );
}

export default NavBar;
