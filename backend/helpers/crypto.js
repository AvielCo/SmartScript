const CryptoJS = require('crypto-js');
require('dotenv').config();

const encryptStrings = (...decryptedStrings) => {
  let encryptedStrings = {};
  decryptedStrings.forEach((decryptedString) => {
    const key = Object.keys(decryptedString);
    const value = Object.values(decryptedString)[0];
    const encryptedString = CryptoJS.AES.encrypt(value, process.env.CRYPTO_SECRET).toString();
    encryptedStrings = { ...encryptedStrings, [key]: JSON.parse(encryptedString) };
  });
  return encryptedStrings;
};

const decryptStrings = (...encryptedStrings) => {
  let decryptedStrings = {};
  encryptedStrings.forEach((encryptedString) => {
    const key = Object.keys(encryptedString);
    const value = Object.values(encryptedString)[0];
    const decryptedString = CryptoJS.AES.decrypt(value, process.env.CRYPTO_SECRET).toString(CryptoJS.enc.Utf8);
    decryptedStrings = { ...decryptedStrings, [key]: decryptedString };
  });
  return decryptedStrings;
};

module.exports = {
  encryptStrings,
  decryptStrings,
};
