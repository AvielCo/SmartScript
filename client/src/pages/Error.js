import React from 'react';
import bookGif from '../assets/book.gif';
import './Error.css';

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
          </div>
        </div>
      </div>
    );
}

export default Error;

