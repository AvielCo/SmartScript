import React from 'react';
import { Button } from '@material-ui/core';
import './NavButton.css';

function NavButton({ btnText, Link, path, onClick }) {
  return (
    <div>
      <Button component={Link} to={path} onClick={onClick}>
        {btnText}
      </Button>
    </div>
  );
}

export default NavButton;
