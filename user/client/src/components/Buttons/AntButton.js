import React from 'react';
import './AntButton.css';
import { Button } from 'antd';

function InputButton({ label, type, component, loading }) {
  return (
    <Button className='btn' component={component} type={type}>
      {console.log(loading)}
      {label}
    </Button>
  );
}
export default InputButton;
