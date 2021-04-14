const express = require('express');
const router = express.Router();
const User = require('../../../models/User');
const History = require('../../../models/History');
const createError = require('http-errors');
const { verifyAccessToken } = require('../../../helpers/jwt');

router.get('/get-all-users', async (req, res, next) => {
  try {
    let users = await User.find();
    if (users.length <= 0) {
      return res.status(204);
    }
    const usersHistories = [];
    for (const user of users) {
      const { _id, banned, email, username, name } = user;
      const userHistory = { _id, banned, email, username, name };
      const {
        predictedResult: { classes, probabilities, dates },
      } = await History.findById({ _id: user.historyId });
      if (classes && classes.length > 0) {
        const h = [];
        for (let i = 0; i < classes.length; i++) {
          console.log(`user: ${user.name} history: ${i}`);
          h.push({ class: classes[i], probability: probabilities[i], date: dates[i] });
        }
        userHistory.history = h;
      }
      usersHistories.push(userHistory);
    }

    res.status(200).json(usersHistories);
  } catch (err) {
    next(err);
  }
});

router.post('/edit-ban', async (req, res, next) => {
  try {
    const { userId, ban, banReason } = req.body;
    if (!userId) {
      throw createError.BadRequest();
    }
    const user = await User.findByIdAndUpdate({ _id: userId }, { banned: ban, banReason });
    if (!user) {
      return res.status(204).send('User not found');
    }
    return res.status(200).json('OK');
  } catch (err) {
    next(err);
  }
});

module.exports = router;
