const JWT = require("jsonwebtoken");
const createError = require("http-errors");
const User = require("../models/User");
const redis = require("./redis");
require("dotenv").config();

const EXP_TIME = 5184000; //60 days

const checkIfUserIsBanned = async (userId, isAdmin) => {
  if (isAdmin) {
    return false;
  }
  const user = await User.findById(userId);
  if (user.banned) {
    return true;
  }
  return false;
};

const signAccessToken = (userId) => {
  return new Promise((resolve, reject) => {
    const payload = {};
    const secret = process.env.JWT_SECRET;
    const options = {
      expiresIn: "60d",
      audience: userId,
    };
    JWT.sign(payload, secret, options, (err, token) => {
      if (err) {
        console.log(err);
        reject(createError.InternalServerError());
      }
      redis.SET(userId, token, "EX", EXP_TIME, (error, reply) => {
        if (error) {
          console.log(error);
          return reject(createError.InternalServerError());
        }
        resolve(token);
      });
    });
  });
};

const verifyAccessToken = async (req, res, next) => {
  const { originalUrl } = req;
  if (!req.headers["authorization"] && originalUrl === "/api/images/predict") {
    return next();
  } else if (!req.headers["authorization"]) {
    return next(createError.Unauthorized());
  }
  const authHeader = req.headers["authorization"];
  const bearerToken = authHeader.split(" ");
  const token = bearerToken[1];
  JWT.verify(token, process.env.JWT_SECRET, (err, payload) => {
    if (err) {
      const message = err.name === "JsonWebTokenError" ? "Unauthorized" : err.message;
      return next(createError.Unauthorized(message));
    }
    const userId = payload["aud"];
    redis.GET(userId, (error, reply) => {
      if (error) {
        console.log(error);
        return next(createError.InternalServerError()); //500
      }
      if (!reply || token !== reply) {
        return next(createError.Unauthorized()); //401
      }
      const isAdmin = req.headers["isadmin"] === "true" ? true : false;
      checkIfUserIsBanned(userId, isAdmin).then((banned) => {
        if (banned) {
          return next(createError.Forbidden()); //403
        }
        req.payload = payload;
        next();
      });
    });
  });
};

module.exports = {
  signAccessToken,
  verifyAccessToken,
};
