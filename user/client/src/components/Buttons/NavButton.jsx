import React from 'react';
import { Button } from '@material-ui/core';
import './NavButton.css';

function NavButton({ btnText,Link, path}) {
  return (
    <div>
      <Button component={Link} to={path} >{btnText}</Button>
    </div>
  );
}

export default NavButton;
