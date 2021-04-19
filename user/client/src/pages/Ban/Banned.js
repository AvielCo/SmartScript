import React from 'react';
import './Banned.css';
import stopsign from '../../assets/stop.png';

function Banned() {
  return (
    <React.Fragment>
      <div className="ban-holder">
        <div className="title-container">
          <h2>403</h2>
        </div>
        <div className="stop-container">
          <img className="stop-image" src={stopsign} alt="stop" />
        </div>
        <div className="title-container">
          <h3>ACCSESS DENIED</h3>
        </div>
      </div>
    </React.Fragment>
  );
}
export default Banned;
