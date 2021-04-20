import React from 'react';
import './ProfileImage.css';
import def from '../../assets/def.jpg';

function ProfileImage({ image }) {
  return (
    <div className='upper-container'>
      <div className='image-container'>
        <img src={image ? image : def} alt='Profile'></img>
      </div>
    </div>
  );
}

export default ProfileImage;
