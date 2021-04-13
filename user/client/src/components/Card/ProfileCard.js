import React from "react";
import ProfileImage from "./ProfileImage";
import ProfileDesc from "./ProfileDesc";
import "./ProfileCard.css";

function ProfileCard() {
  return (
    <div className="profile-container">
      <ProfileImage />
      <ProfileDesc />
    </div>
  );
}

export default ProfileCard;
