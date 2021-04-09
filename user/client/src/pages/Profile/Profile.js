import React, { useState, useEffect } from 'react';
import { RoundImage, NavBar, List, Searchbar } from '../../components';
import EdiText from 'react-editext';
import axios from 'axios';
import { Skeleton } from 'antd';
import { useHistory } from 'react-router-dom';
import { getAccessToken } from '../../helpers';

import './Profile.css';

function Profile() {
  const [userData, setUserData] = useState({
    details: {
      email: '',
      username: '',
      name: '',
    },
    history: [],
  });
  const [loadingData, setLoadingData] = useState(true);
  const [query, setQuery] = useState({ searchBy: [], searchType: 'none' });
  const history = useHistory();
  const handleChanges = (value, fieldName) => {
    //! handle change of one of the fields by sending a request to the backend.
    console.log(value, fieldName);
  };

  const TextFieldsHolder = () => {
    //* example on how the data foramt should look like

    const textFields = [
      { label: 'Email', value: userData.details.email },
      { label: 'Username', value: userData.details.username },
      { label: 'Name', value: userData.details.name },
    ];
    return (
      <div className="profile-textfields">
        {textFields.map((textField) => {
          return (
            <div className="textfield">
              <label>
                <u>{textField.label}</u>
              </label>
              <h4>{textField.value}</h4>
            </div>
          );
        })}
      </div>
    );
  };

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
          let { details, history } = res.data;
          history = history.map((event) => {
            const base64image = event.image;
            const byteCharacters = atob(base64image);
            const byteNumbers = new Array(byteCharacters.length);
            for (let i = 0; i < byteCharacters.length; i++) {
              byteNumbers[i] = byteCharacters.charCodeAt(i);
            }
            const byteArray = new Uint8Array(byteNumbers);

            const imageBlob = new Blob([byteArray], { type: 'image/jpeg' });
            const image = URL.createObjectURL(imageBlob);
            event.image = image;
            return event;
          });
          setLoadingData(false);
          console.log(history);
          setUserData({ details, history });
        }
      })
      .catch((err) => {
        console.log(err);
      });
  }, []);

  return (
    <div className="profile-page">
      <NavBar />
      <div className="profile-form">
        <TextFieldsHolder />
        {/* picture property should be an object, not url */}
        {/* <RoundImage picture={aviel} /> */}
      </div>
      <div className="history-container">
        <Searchbar setQuery={setQuery} />
        <Skeleton loading={loadingData} active round>
          <List data={userData.history} query={query} />
        </Skeleton>
      </div>
    </div>
  );
}

export default Profile;
