const express = require('express');
const router = express.Router();
const User = require('../../../models/User');
const createError = require('http-errors');
const { verifyAccessToken } = require('../../../helpers/jwt');

router.get('/get-all-users', async (req, res, next) => {
  try {
    const users = await User.find();
    if (users.length <= 0) {
      return res.status(204);
    }
    res.status(200).json(users);
  } catch (err) {
    next(err);
  }
});

router.post('/ban-user', async (req, res, next) => {
  try {
    if (!req.body.userId) {
      throw createError.BadRequest();
    }
    const user = await User.findByIdAndUpdate({ _id: req.body.userId }, { banned: true });
    if (!user) {
      return res.status(204).send('User not found');
    }
    return res.status(200).json('User banned');
  } catch (err) {
    next(err);
  }
});

router.post('/unban-user', async (req, res, next) => {
  try {
    if (!req.body.userId) {
      throw createError.BadRequest();
    }
    const user = await User.findByIdAndUpdate({ _id: req.body.userId }, { banned: false });
    if (!user) {
      return res.status(204).send('User not found');
    }
    return res.status(200).json('User unbanned');
  } catch (err) {
    next(err);
  }
});

router.post('/user-profile', async (req, res, next) => {
  try {
    if (!req.body.userId) {
      throw createError.BadRequest();
    }
    const user = await User.findById({ _id: req.body.userId });
    if (!user) {
      return res.status(204).send('User not found');
    }
    return res.status(200).json(user);
  } catch (err) {
    next(err);
  }
});

module.exports = router;
