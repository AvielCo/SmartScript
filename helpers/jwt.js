const JWT = require('jsonwebtoken');
const createError = require('http-errors');
const User = require('../models/User');
require('dotenv').config();

const checkIfUserIsBanned = async (userId) => {
  const user = await User.findById(userId);
  if (user.banned) {
    return true;
  }
  return false;
};

const signAccessToken = (userId) => {
  return new Promise(async (resolve, reject) => {
    const payload = {};
    const secret = process.env.JWT_SECRET;
    const options = {
      expiresIn: '1y',
      audience: userId,
    };
    JWT.sign(payload, secret, options, (err, token) => {
      if (err) {
        reject(createError.InternalServerError());
      }
      resolve(token);
    });
  });
};

const verifyAccessToken = (req, res, next) => {
  if (!req.headers['authorization']) {
    return next(createError.Unauthorized());
  }
  const authHeader = req.headers['authorization'];
  const bearerToken = authHeader.split(' ');
  const token = bearerToken[1];
  JWT.verify(token, process.env.JWT_SECRET, (err, payload) => {
    if (err) {
      const message = err.name === 'JsonWebTokenError' ? 'Unauthorized' : err.message;
      return next(createError.Unauthorized(message));
    }
    const userId = payload['aud'];
    checkIfUserIsBanned(userId).then((banned) => {
      if (banned) {
        return next(createError.Forbidden());
      }
      req.payload = payload;
      next();
    });
  });
};

module.exports = {
  signAccessToken,
  verifyAccessToken,
};
