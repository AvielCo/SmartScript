import React from 'react';
import ProfileImage from './ProfileImage';
import ProfileDesc from './ProfileDesc';
import './ProfileCard.css';

function ProfileCard({ name, image, text }) {
  return (
    <div className='profile-container'>
      <ProfileImage image={image} />
      <ProfileDesc name={name} text={text}/>
    </div>
  );
}

export default ProfileCard;
