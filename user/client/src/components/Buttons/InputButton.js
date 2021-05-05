import React from 'react';
import './InputButton.css';
import { Button, CircularProgress } from '@material-ui/core';

function InputButton(props) {
  return (
    <div>
      <Button variant='contained' type={props.type} component={props.component} onClick={props.onClick}>
        {props.name}
        {props.disabled && <CircularProgress className='loader' />}
      </Button>
    </div>
  );
}
export default InputButton;
