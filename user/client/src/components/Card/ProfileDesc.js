import React from 'react';
import './ProfileDesc.css';

function ProfileDesc({ name, text }) {
  return (
    <div className='lower-container'>
      <h3>{name}</h3>
      <p>{text}</p>
    </div>
  );
}

export default ProfileDesc;
