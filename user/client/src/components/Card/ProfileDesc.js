import React from 'react';
import './ProfileDesc.css';

import Github from '../../assets/github.svg';
import Linkedin from '../../assets/linkedin.svg';

function ProfileDesc({ name, github_link, linkedin_link }) {
  return (
    <div className='lower-container'>
      <h3>{name}</h3>
      <div className='icon-holder'>
        <div className='icon github'>
          <a href={github_link} target='_blank'>
            <img src={Github} />
          </a>
        </div>
        <div className='icon linkedin'>
          <a href={linkedin_link} target='_blank'>
            <img src={Linkedin} />
          </a>
        </div>
      </div>
    </div>
  );
}

export default ProfileDesc;
