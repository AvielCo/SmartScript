import React from 'react';
import bookGif from '../../assets/book.gif';
import './NotFound.css';
// import Home from '../Home/Home';
import { BrowserRouter as Router } from "react-router-dom";
import Button from "@material-ui/core/Button";

function Error() {
    return (
      <div className="error-holder">
        <div className="error-container">
          <div className="error-title">
            <h1>4</h1>
            <img src={bookGif} alt="book-gif" className="gif" />
            <h1>4</h1>
          </div>
          <div className="error-content">
            <h2>Error:404 page not found</h2>
            <p>Sorry, the page you are looking for cannot be found</p>
            {/* <Button className="back-home-btn" component={Home} to="/home"> */}
              Home
            {/* </Button> */}
          </div>
        </div>
      </div>
    );
}

export default Error;

