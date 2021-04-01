import React from 'react';
//import TextField from "@material-ui/core/TextField";
import './InputField.css';
import { Input } from 'antd';

function InputField({ value, type, name, setProperty, prefix }) {
  return (
    <Input
      size='large'
      className='input-field'
      placeholder={value}
      type={type}
      name={name}
      onChange={(event) => {
        setProperty(event.target.value);
      }}
      prefix={prefix}
    />
  );
}
export default InputField;
