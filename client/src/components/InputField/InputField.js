import React from 'react';
import TextField from "@material-ui/core/TextField";
import './InputField.css';


function InputField({ name }) {
  return (
    <div>
      <TextField
        variant="outlined"
        required
        label={name} 
        className="input-field">
        {name}
      </TextField>
    </div>
  );
}
export default InputField;