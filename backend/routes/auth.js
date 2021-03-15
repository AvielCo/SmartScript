const express = require('express');
const router = express.Router();
const User = require('../models/User');
const History = require('../models/History');
const createError = require('http-errors');
const bcrypt = require('bcrypt');
const authSchema = require('../validations/auth');
const { signAccessToken } = require('../helpers/jwt');

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
        throw createError.Conflict('Username is already exists');
      }
      if (userExists.email === newUserDetails.email) {
        throw createError.Conflict('Email is already exists');
      }
      throw createError.Conflict();
    }

    //* User is not exists with the same email or username
    const newUser = await new User(newUserDetails).save();
    await new History({ userId: newUser._id }).save();

    //* Generate access token
    return res.status(200).json('Registered successfully');
  } catch (err) {
    if (err.isJoi) {
      err.status = 422;
    }
    next(err);
  }
});

router.post('/login', async (req, res, next) => {
  try {
    const user = await User.findOne({ username: req.query.username });
    //TODO: validate password with DBc
    console.log(user);
    const accessToken = await signAccessToken(user.id);
    res.status(200).json(accessToken);
  } catch (err) {
    next(err);
  }
});

module.exports = router;
