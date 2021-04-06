import React, { useState, useEffect } from 'react';
import { RoundImage, NavBar, List } from '../../components';
import EdiText from 'react-editext';
import axios from 'axios';
import './Profile.css';

function Profile() {
  const [userData, setUserData] = useState({});
  const handleChanges = (value, fieldName) => {
    //! handle change of one of the fields by sending a request to the backend.
    console.log(value, fieldName);
  };

  const TextFieldsHolder = () => {
    //* example on how the data foramt should look like
    const textFields = [
      { label: 'Email', name: 'email', value: userData.details.email, hint: 'Press enter to save changes.', type: 'email', index: 3 },
      { label: 'Username', name: 'username', value: userData.details.username, hint: 'Press enter to save changes.', index: 1 },
      { label: 'Name', name: 'name', value: userData.details.name, hint: 'Press enter to save changes.', index: 2 },
    ];
    return (
      <div className='profile-textfields'>
        {textFields.map((textField) => {
          return (
            <div className='textfield'>
              <label>
                <u>{textField.label}</u>
              </label>
              <EdiText
                value={textField.value}
                hint={textField.hint}
                type={textField.type ? textField.type : 'text'}
                inputProps={textField.name}
                saveButtonClassName='hidden-btn'
                cancelButtonClassName='hidden-btn'
                editButtonClassName='hidden-btn'
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

  //TODO: use useEffect to get current user details with the accesstoken inside session storage(if exists).

  useEffect(() => {
    let accessToken = getAccessToken();

    const cfg = {
      headers: {
        Authorization: 'Bearer ' + accessToken,
      },
    };
    axios
      .get('http://localhost:8008/api/profile', cfg)
      .then((res) => {
        if (res.status === 200) {
          setUserData(res.data.userData);
        }
      })
      .catch((err) => {
        if (err.response) {
          const { status, message } = err.response.data.error;
          if (status === 404) {
            history.replace('/404');
            return;
          }
          alert(message);
        } else {
          alert('Internal Server Error');
        }
      });
  }, []);
  return (
    <div className='profile-page'>
      <NavBar />
      <div className='profile-form'>
        <TextFieldsHolder />
        {/* picture property should be an object, not url */}
        {/* <RoundImage picture={aviel} /> */}
      </div>
      <List data={userData.history} />
    </div>
  );
}

export default Profile;
