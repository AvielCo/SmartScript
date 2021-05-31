import React from "react";
import "./InputButton.css";
import { Button, CircularProgress } from "@material-ui/core";

function InputButton({ name, type, component, onClick, disabled }) {
  return (
    <div>
      <Button variant="contained" type={type} component={component} onClick={onClick} disabled={disabled}>
        {name}
      </Button>
    </div>
  );
}
export default InputButton;
