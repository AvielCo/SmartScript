import React from 'react';
import NavButton from '../Buttons/NavButton';
import logo from '../../assets/smartscript-logo.png';
import axios from 'axios';
import { useState } from 'react';
import { Link } from 'react-router-dom';
import './NavBar.css';
import { HashLink as HashLink } from 'react-router-hash-link';
import { getAccessToken } from '../../helpers';
import { useHistory } from 'react-router-dom';

function NavBar({ isLoggedIn, setIsLoggedIn }) {
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
      },
    };

    axios
      .delete(`http://${process.env.REACT_APP_API_ADDRESS}:8008/api/auth/logout`, cfg)
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

  return (
    <nav className='navbar' position='sticky'>
      <Link className='logo' to='/home'>
        <img alt='SmartScript-logo' src={logo} />
      </Link>
      <div className={slide ? 'navbar-holder active' : 'navbar-holder'} slide={slide}>
        <HashLink to="home#scan" style={{ textDecoration: 'none' }} smooth>
          <NavButton className="nav-button" btnText="Scan" />
        </HashLink>
        <HashLink to="home#about" style={{ textDecoration: 'none' }} smooth>
          <NavButton className="nav-button" btnText="About" />
        </HashLink>
        <HashLink to="home#wwa" style={{ textDecoration: 'none' }} smooth>
          <NavButton className="nav-button" btnText="Who we are" />
        </HashLink>
        {!isLoggedIn && (
          <Link to='/login' style={{ textDecoration: 'none' }}>
            <NavButton className='nav-button' btnText='Login' />
          </Link>
        )}
        {!isLoggedIn && (
          <Link to='/register' style={{ textDecoration: 'none' }}>
            <NavButton className='nav-button' btnText='Register' />
          </Link>
        )}
        {isLoggedIn && (
          <Link to='/profile' style={{ textDecoration: 'none' }}>
            <NavButton className='nav-button' btnText='Profile' />
          </Link>
        )}

        {isLoggedIn && (
          <Link to='/home' style={{ textDecoration: 'none' }}>
            <NavButton className='nav-button' btnText='Logout' onClick={() => logout()} />{' '}
          </Link>
        )}
      </div>
      <div onClick={showSidebar} className={slide ? 'burger cross' : 'burger'} id='burger'>
        <div className='line-1'></div>
        <div className='line-2'></div>
        <div className='line-3'></div>
      </div>
    </nav>
  );
}

export default NavBar;
