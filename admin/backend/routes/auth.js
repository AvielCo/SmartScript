const express = require('express');
const router = express.Router();
const Admin = require('../../../models/Admin');
const createError = require('http-errors');
const { decryptStrings } = require('../../../helpers/crypto');
const { signAccessToken, signRefreshToken, verifyRefreshToken, verifyAccessToken } = require('../../../helpers/jwt');
require('dotenv').config();

router.post('/login', async (req, res, next) => {
  try {
    const { username, password } = decryptStrings({ username: req.body.username }, { password: req.body.password });
    const admin = await Admin.findOne({ username }).select('+password');

    const isMatch = await admin.isValidPassword(password);
    if (!isMatch) {
      throw createError.Unauthorized('Username or password are incorrect.');
    }

    await signAccessToken(admin.id);
    await signRefreshToken(admin.id);

    res.status(200);
  } catch (err) {
    if (err.isJoi) {
      return next(createError.BadRequest('Invalid username or password.'));
    }
    next(err);
  }
});

router.get('/user', verifyAccessToken, (req, res, next) => {
  const userId = req.payload['aud'];
  return res.status(200).json('OK');
});

router.post('/refresh-token', async (req, res, next) => {
  try {
    const { refreshToken } = req.body;
    if (!refreshToken) {
      throw createError.BadRequest();
    }
    const userId = await verifyRefreshToken(refreshToken);

    await signAccessToken(userId);
    await signRefreshToken(userId);

    res.status(200).send('New access and refresh tokens has been generated.');
  } catch (err) {
    next(err);
  }
});

module.exports = router;
