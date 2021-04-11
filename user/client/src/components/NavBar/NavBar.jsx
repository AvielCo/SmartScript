import React from 'react';
import NavButton from '../Buttons/NavButton';
import logo from '../../assets/smartscript-logo.png';
import { useState } from 'react';
import { Link } from 'react-router-dom';
import './NavBar.css';

function NavBar({ isLoggedIn }) {
  const [slide, setSlide] = useState(0);
  const showSidebar = () => setSlide(!slide);

  return (
    <nav className="navbar" position="sticky">
      <Link className="logo" to="/home">
        <img alt="SmartScript-logo" src={logo} />
      </Link>
      <div className={slide ? 'navbar-holder active' : 'navbar-holder'} slide={slide}>
        {/* <div className="btnGroup"> */}
        <NavButton className="nav-button" btnText="Scan" />
        <NavButton className="nav-button" btnText="About" />
        <NavButton className="nav-button" btnText="Who we are" />
        {!isLoggedIn && (
          <Link to="/login" style={{ textDecoration: 'none' }}>
            <NavButton className="nav-button" btnText="Login" />
          </Link>
        )}
        {!isLoggedIn && (
          <Link to="/register" style={{ textDecoration: 'none' }}>
            <NavButton className="nav-button" btnText="Register" />
          </Link>
        )}
        {isLoggedIn && (
          <Link to="/profile" style={{ textDecoration: 'none' }}>
            <NavButton className="nav-button" btnText="Profile" />
          </Link>
        )}
        {isLoggedIn && (
          <Link to="/logout" style={{ textDecoration: 'none' }}>
            <NavButton className="nav-button" btnText="Logout" />
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
