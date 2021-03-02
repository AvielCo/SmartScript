import React from "react";
import "./InputButton.css";
import { Button } from "@material-ui/core";

function InputButton({ name }) {
  return (
    <div>
      <Button variant="contained">{name}</Button>
    </div>
  );
}
export default InputButton;
