const express = require('express');
const router = express.Router();
const Admin = require('../../../models/Admin');
const createError = require('http-errors');
const { decryptStrings } = require('../../../helpers/crypto');
const redis = require('../../../helpers/redis');
const { signAccessToken, verifyAccessToken } = require('../../../helpers/jwt');
require('dotenv').config();

router.post('/login', async (req, res, next) => {
  try {
    const { username, password } = decryptStrings({ username: req.body.username }, { password: req.body.password });
    const admin = await Admin.findOne({ username }).select('+password');

    const isMatch = await admin.isValidPassword(password);
    if (!isMatch) {
      throw createError.Unauthorized('Username or password are incorrect.');
    }

    const accessToken = await signAccessToken(admin.id);

    res.status(200).json({ accessToken });
  } catch (err) {
    if (err.isJoi) {
      return next(createError.BadRequest('Invalid username or password.'));
    }
    next(err);
  }
});

router.get('/user', verifyAccessToken, (req, res, next) => {
  try {
    return res.sendStatus(200);
  } catch (err) {
    next(err);
  }
});

router.delete('/logout', verifyAccessToken, (req, res, next) => {
  try {
    const userId = req.payload['aud'];
    redis.DEL(userId, (error, reply) => {
      if (error) {
        throw createError.InternalServerError();
      }
      res.sendStatus(204);
    });
  } catch (err) {
    next(err);
  }
});

module.exports = router;
