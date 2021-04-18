import React from 'react';
import './InputButton.css';
import { Button, CircularProgress } from '@material-ui/core';

function InputButton({ name, type, component, onClick, disabled }) {
  return (
    <div>
      <Button variant='contained' type={type} component={component} onClick={onClick}>
        {name}
        {console.log(disabled)}
        {disabled && <CircularProgress className="loader" />}
      </Button>
    </div>
  );
}
export default InputButton;
