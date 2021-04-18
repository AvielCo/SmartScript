import React, { useState, useEffect } from 'react';
import { NavBar, List, Searchbar } from '../../components';
import { ToastContainer, toast } from 'react-toastify';
import axios from 'axios';
import { Skeleton } from 'antd';
import { getAccessToken } from '../../helpers';

import 'react-toastify/dist/ReactToastify.css';
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
  const [isDataChanged, setIsDataChanged] = useState(true);
  const [query, setQuery] = useState({ searchBy: [], searchType: 'none' });

  const TextFieldsHolder = () => {
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

  const removeItemFromHistory = (indexToDelete) => {
    if (indexToDelete < 0) {
      return;
    }
    setLoadingData(true);
    const cfg = {
      headers: {
        Authorization: 'Bearer ' + getAccessToken(),
      },
    };
    axios
      .delete(`http://${process.env.REACT_APP_API_ADDRESS}:8008/api/profile/delete-event/${indexToDelete}`, cfg)
      .then((res) => {
        if (res.status === 200) {
          setIsDataChanged(true);
        }
      })
      .catch((err) => console.log(err));
  };

  useEffect(() => {
    if (!isDataChanged) return;
    let accessToken = getAccessToken();

    const cfg = {
      headers: {
        Authorization: 'Bearer ' + accessToken,
      },
    };
    axios
      .get(`http://${process.env.REACT_APP_API_ADDRESS}:8008/api/profile`, cfg)
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
          setUserData({ details, history });
          setIsDataChanged(false);
        }
      })
      .catch((err) => {
        toast('Internal Server Error.');
      });
  }, [isDataChanged]);

  return (
    <>
      <ToastContainer position="top-left" autoClose={5000} hideProgressBar={false} newestOnTop closeOnClick rtl={false} pauseOnFocusLoss draggable pauseOnHover />
      <div className="profile-page">
        <NavBar />
        <div className="profile-form">
          <TextFieldsHolder />
        </div>
        <div className="history-container">
          <Searchbar setQuery={setQuery} />
          <Skeleton loading={loadingData} active round>
            <List data={userData.history} query={query} removeItem={removeItemFromHistory} />
          </Skeleton>
        </div>
      </div>
    </>
  );
}

export default Profile;
