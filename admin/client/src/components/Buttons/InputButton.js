import React from 'react';
import './InputButton.css';
import { Button } from '@material-ui/core';

function InputButton({ name, type, component, onClick }) {
  return (
    <div>
      <Button variant="contained" type={type} component={component} onClick={onClick}>
        {name}
      </Button>
    </div>
  );
}
export default InputButton;
