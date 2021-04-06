const express = require('express');
const router = express.Router();
const User = require('../../../models/User');
const History = require('../../../models/History');
const createError = require('http-errors');
const fs = require('fs');
const path = require('path');
const buffer = require('buffer');
const authSchema = require('../validations/auth');
const { verifyAccessToken } = require('../../../helpers/jwt');
require('dotenv').config();

router.get('/', verifyAccessToken, async (req, res, next) => {
  try {
    const userId = req.payload['aud'];
    const user = await User.findById(userId);
    const {
      predictedResult: { classes, dates, probabilities },
    } = await History.findById(user.historyId);
    const imagesPath = path.join(process.cwd(), 'users-histories', req.payload.aud);
    const userData = {
      details: {
        email: user.email,
        username: user.username,
        name: user.name,
      },
      history: [],
    };
    for (let i = 0; i < classes.length; i++) {
      const imageContent = fs.readFileSync(path.join(imagesPath, `${i}.jpg`), 'base64');
      const history = {
        class: classes[i],
        probability: probabilities[i],
        dates: dates[i],
        image: imageContent,
      };
      userData.history.push(history);
    }
    res.send(userData);
  } catch (err) {
    next(err);
  }
});

router.post('/', verifyAccessToken, (req, res, next) => {});

module.exports = router;
