import CryptoJS from 'crypto-js';

export const encryptStrings = (...decryptedStrings) => {
  let encryptedStrings = {};
  decryptedStrings.forEach((decryptedString) => {
    const key = Object.keys(decryptedString);
    const value = Object.values(decryptedString)[0];
    const encryptedString = CryptoJS.AES.encrypt(value, process.env.REACT_APP_CRYPTO_SECRET).toString();
    encryptedStrings = { ...encryptedStrings, [key]: encryptedString };
  });
  return encryptedStrings;
};

export const decryptStrings = (...encryptedStrings) => {
  let decryptedStrings = {};
  encryptedStrings.forEach((encryptedString) => {
    const key = Object.keys(encryptedString);
    const value = Object.values(encryptedString)[0];
    const decryptedString = CryptoJS.AES.decrypt(value, process.env.CRYPTO_SECRET).toString(CryptoJS.enc.Utf8);
    decryptedStrings = { ...decryptedStrings, [key]: decryptedString };
  });
  return decryptedStrings;
};

export const getAccessToken = () => {
  let accessToken = window.sessionStorage.getItem('accessToken');
  if (!accessToken) {
    accessToken = window.localStorage.getItem('accessToken');
  }
  return accessToken;
};
