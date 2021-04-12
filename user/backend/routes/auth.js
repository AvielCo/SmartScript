const express = require('express');
const router = express.Router();
const User = require('../../../models/User');
const History = require('../../../models/History');
const createError = require('http-errors');
const authSchema = require('../validations/auth');
const { decryptStrings } = require('../../../helpers/crypto');
const { signAccessToken, verifyAccessToken } = require('../../../helpers/jwt');
require('dotenv').config();

router.post('/register', async (req, res, next) => {
  try {
    const { email, username, password, name } = decryptStrings({ email: req.body.email }, { username: req.body.username }, { password: req.body.password }, { name: req.body.name });
    if (!email || !username || !password || !name) {
      throw createError.BadRequest();
    }
    await authSchema.validateAsync({ email, username, password, name });

    const newUserDetails = {
      email,
      username,
      password,
      name,
    };

    //* Check if user exists
    const userExists = await User.findOne({
      $or: [{ email: newUserDetails.email }, { username: newUserDetails.username }],
    });

    if (userExists) {
      //! User is exists
      //! Check which fields are the same and throw an error
      if (userExists.username === newUserDetails.username) {
        throw createError.Conflict('Username is already in use.');
      }
      if (userExists.email === newUserDetails.email) {
        throw createError.Conflict('Email is already in use.');
      }
      throw createError.Conflict();
    }

    //* User is not exists with the same email or username
    const newUser = await new User(newUserDetails).save();
    const history = await new History({ userId: newUser._id, predictedResult: { classes: [], probabilities: [], dates: [] } }).save();

    newUser.update({ historyId: history._id });
    await newUser.save();

    await signAccessToken(newUser.id);

    res.status(200).send('Registered user successfully.');
  } catch (err) {
    if (err.isJoi) {
      err.status = 422;
    }
    next(err);
  }
});

router.post('/login', async (req, res, next) => {
  try {
    const { username, password } = decryptStrings({ username: req.body.username }, { password: req.body.password });
    const user = await User.findOne({ username }).select('+password');

    const isMatch = await user.isValidPassword(password);
    if (!isMatch) {
      throw createError.Unauthorized('Username or password are incorrect.');
    }

    const accessToken = await signAccessToken(user.id);

    res.status(200).json({ accessToken });
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

module.exports = router;
