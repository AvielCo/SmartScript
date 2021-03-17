const express = require('express');
const router = express.Router();
const User = require('../models/User');
const History = require('../models/History');
const createError = require('http-errors');
const authSchema = require('../validations/auth');
const { decryptStrings } = require('../helpers/crypto');
const { signAccessToken, signRefreshToken, verifyRefreshToken } = require('../helpers/jwt');
require('dotenv').config();

router.get('/get-all', async (req, res) => {
  try {
    const users = await User.find();
    res.status(200).json(users);
  } catch (err) {
    res.json({ message: err });
  }
});

router.post('/register', async (req, res, next) => {
  try {
    const { email, username, password, name } = req.body;
    if (!email || !username || !password || !name) {
      throw createError.BadRequest();
    }

    await authSchema.validateAsync(req.body);

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
    const history = await new History({ userId: newUser._id }).save();

    await User.findOneAndUpdate({ _id: newUser._id }, { historyId: history._id });

    await signAccessToken(newUser.id);
    await signRefreshToken(newUser.id);

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
    const { username, password } = decryptStrings({ username: req.query.username }, { password: req.query.password });
    const user = await User.findOne({ username }).select('+password');
    console.log(user)
    console.log(password)
    const isMatch = await user.isValidPassword(password);
    if (!isMatch) {
      throw createError.Unauthorized('Username or password are incorrect.');
    }

    await signAccessToken(user.id);
    await signRefreshToken(user.id);

    res.status(200).send('Login success.');
  } catch (err) {
    if (err.isJoi) {
      return next(createError.BadRequest('Invalid username or password.'));
    }
    next(err);
  }
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

    res.status(200);
  } catch (err) {
    next(err);
  }
});

module.exports = router;
