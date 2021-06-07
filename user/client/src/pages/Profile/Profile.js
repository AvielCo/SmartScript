import React, { useState, useEffect } from "react";
import { List, Searchbar } from "../../components";
import { toast } from "react-toastify";
import { Redirect } from "react-router";
import axios from "axios";
import { Skeleton } from "antd";
import { getAccessToken } from "../../helpers";

import "react-toastify/dist/ReactToastify.css";
import "./Profile.css";

function Profile({ isLoggedIn }) {
  const [userData, setUserData] = useState({
    details: {
      email: "",
      username: "",
    },
    history: [],
  });
  const [loadingData, setLoadingData] = useState(true);
  const [isDataChanged, setIsDataChanged] = useState(true);
  const [query, setQuery] = useState({ searchBy: [], searchType: "none" });

  const TextFieldsHolder = () => {
    const textFields = [
      { label: "Email", value: userData.details.email },
      { label: "Username", value: userData.details.username },
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
        Authorization: "Bearer " + getAccessToken(),
      },
    };
    axios
      .delete(`${process.env.REACT_APP_API_ADDRESS}/api/profile/event/${indexToDelete}`, cfg)
      .then((res) => {
        if (res.status === 200) {
          setIsDataChanged(true);
        }
      })
      .catch((err) => console.log(err));
  };

  useEffect(() => {
    if (!isDataChanged) return;

    const cfg = {
      headers: {
        Authorization: "Bearer " + getAccessToken(),
      },
    };

    axios
      .get(`${process.env.REACT_APP_API_ADDRESS}/api/profile`, cfg)
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
            const imageBlob = new Blob([byteArray], { type: "image/jpeg" });
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
        setLoadingData(false);
        toast("Internal Server Error.");
      });
  }, [isDataChanged]);

  return (
    <React.Fragment>
      {!isLoggedIn ? (
        <Redirect to="/home" />
      ) : (
        <div className="profile-page">
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
      )}
    </React.Fragment>
  );
}

export default Profile;
