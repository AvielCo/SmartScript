const JWT = require('jsonwebtoken');
const createError = require('http-errors');
const redisClient = require('./redis');
require('dotenv').config();

const YEAR = 60 * 60 * 24 * 365;

const signAccessToken = (userId) => {
  return new Promise((resolve, reject) => {
    const payload = {};
    const secret = process.env.JWT_SECRET;
    const options = {
      expiresIn: '60d',
      audience: userId,
    };
    JWT.sign(payload, secret, options, (err, token) => {
      if (err) {
        console.log(err);
        reject(createError.InternalServerError());
      }
      resolve(token);
    });
  });
};

const signRefreshToken = (userId) => {
  return new Promise((resolve, reject) => {
    const payload = {};
    const secret = process.env.REFRESH_TOKEN_SECRET;
    const options = {
      expiresIn: '1y',
      audience: userId,
    };
    JWT.sign(payload, secret, options, (err, token) => {
      if (err) {
        console.log(err);
        reject(createError.InternalServerError());
      }
      redisClient.SET(userId, token, 'EX', YEAR, (err, reply) => {
        if (err) {
          return reject(createError.InternalServerError());
        }
        resolve(token);
      });
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
    req.payload = payload;
    next();
  });
};

const verifyRefreshToken = (refToken) => {
  return new Promise((resolve, reject) => {
    JWT.verify(refToken, process.env.REFRESH_TOKEN_SECRET, (err, payload) => {
      if (err) {
        return reject(createError.Unauthorized());
      }
      const userId = payload.aud;
      redisClient.GET(userId, (err, result) => {
        if (err) {
          return reject(createError.InternalServerError());
        }
        return refToken === result ? resolve(userId) : reject(createError.Unauthorized());
      });
    });
  });
};

module.exports = {
  signAccessToken,
  signRefreshToken,
  verifyAccessToken,
  verifyRefreshToken,
};
