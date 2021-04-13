import React from 'react';
import './ProfileImage.css'
import Noah from '../../assets/noah.jpg'

function ProfileImage(){
    return (
        <div className="upper-container">
            <div className="image-container">
                <img src={Noah} alt="Noah Profile"></img>

            </div>
        </div>
              
    );
};

export default ProfileImage;