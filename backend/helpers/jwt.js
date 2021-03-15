const JWT = require('jsonwebtoken');
const createError = require('http-errors');
require('dotenv').config();

const signAccessToken = (userId) => {
  return new Promise((resolve, reject) => {
    const payload = {};
    const secret = process.env.SUPERSECRET;
    const options = {
      audience: userId,
    };
    JWT.sign(payload, secret, options, (err, token) => {
      if (err) {
        return reject(err);
      }
      resolve(token);
    });
  });
};

module.exports = {
  signAccessToken,
};
