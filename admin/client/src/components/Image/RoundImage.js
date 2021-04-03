import React from 'react';
import './RoundImage.css';

function RoundImage({ picture }) {
  const style = {
    backgroundImage: `url(${picture})`,
  };
  return <div style={style} className="round-image"></div>;
}

export default RoundImage;
