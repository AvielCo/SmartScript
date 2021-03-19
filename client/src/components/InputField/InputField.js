import React from 'react';
import TextField from "@material-ui/core/TextField";
import './InputField.css';


function InputField({ value, type ,name, setProperty}) {
  return (
    <div>
      <TextField
        variant="outlined"
        required
        type={type}
        label={value} 
        className="input-field"
        name={name}
        onChange={(event)=> {setProperty(event.target.value)}}>
        {value}
      </TextField>
    </div>
  );
}
export default InputField;