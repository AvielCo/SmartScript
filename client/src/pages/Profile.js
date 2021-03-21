import React, { useState, useEffect } from 'react';
import RoundImage from '../components/Image/RoundImage';
import aviel from '../assets/aviel.jfif';
import EdiText from 'react-editext';
import NavBar from '../components/NavBar/NavBar';
import axios from 'axios';
import './Profile.css';

function Profile() {
  const handleChanges = (value, fieldName) => {
    //! handle change of one of the fields by sending a request to the backend.
    console.log(value, fieldName);
  };

  const TextFieldsHolder = ({ username, email, name }) => {
    //* example on how the data foramt should look like
    const textFields = [
      { label: 'Email', name: 'email', value: email, hint: 'Press enter to save changes.', type: 'email', index: 3 },
      { label: 'Username', name: 'username', value: username, hint: 'Press enter to save changes.', index: 1 },
      { label: 'Name', name: 'name', value: name, hint: 'Press enter to save changes.', index: 2 },
    ];
    return (
      <div className="profile-textfields">
        {textFields.map((textField) => {
          return (
            <div className="textfield">
              <label>
                <u>{textField.label}</u>
              </label>
              <EdiText
                value={textField.value}
                hint={textField.hint}
                type={textField.type ? textField.type : 'text'}
                inputProps={textField.name}
                saveButtonClassName="hidden-btn"
                cancelButtonClassName="hidden-btn"
                editButtonClassName="hidden-btn"
                tabIndex={textField.index}
                onSave={handleChanges}
                cancelOnEscape
                cancelOnUnfocus
                startEditingOnFocus
                submitOnEnter
              />
            </div>
          );
        })}
      </div>
    );
  };

  return (
    <div className="profile-page">
      <NavBar />
      <div className="profile-form">
        <TextFieldsHolder username="AvielCo" email="avielcohen15@gmail.com" name="Aviel Cohen" />
        {/* picture property should be an object, not url */}
        <RoundImage picture={aviel} />
      </div>
    </div>
  );
}

export default Profile;
