import React from 'react';
import ProfileImage from './ProfileImage';
import ProfileDesc from './ProfileDesc';
import './ProfileCard.css';

function ProfileCard({ name, image, github_link, linkedin_link }) {
  return (
    <div className='profile-container'>
      <ProfileImage image={image} />
      <ProfileDesc name={name} github_link={github_link} linkedin_link={linkedin_link} />
    </div>
  );
}

export default ProfileCard;
