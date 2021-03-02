import React from 'react';
import { Button } from '@material-ui/core';
import './NavButton.css';

function NavButton({ btnText }) {
  return (
    <div>
      <Button>{btnText}</Button>
    </div>
  );
}

export default NavButton;
