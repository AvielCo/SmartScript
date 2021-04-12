const express = require('express');
const router = express.Router();
const User = require('../../../models/User');
const History = require('../../../models/History');
const createError = require('http-errors');
const fs = require('fs');
const path = require('path');
const { verifyAccessToken } = require('../../../helpers/jwt');
require('dotenv').config();

router.get('/', verifyAccessToken, async (req, res, next) => {
  try {
    const userId = req.payload['aud'];
    const user = await User.findById(userId);

    const userData = {
      details: {
        email: user.email,
        username: user.username,
        name: user.name,
      },
      history: [],
    };

    const {
      predictedResult: { classes, dates, probabilities },
    } = await History.findById(user.historyId);

    if (!classes || !probabilities || !dates) {
      return res.send(userData);
    }

    const imagesPath = path.join(__dirname, '..', 'users-histories', req.payload.aud);
    console.log(imagesPath);
    for (let i = 0; i < classes.length; i++) {
      const imageContent = fs.readFileSync(path.join(imagesPath, `${i}.jpg`), 'base64');
      console.log(imageContent);
      const history = {
        class: classes[i],
        probability: probabilities[i],
        dates: dates[i],
        image: imageContent,
      };
      console.log(history);
      userData.history.push(history);
    }
    console.log(userData);
    res.send(userData);
  } catch (err) {
    next(err);
  }
});

router.delete('/delete-event', verifyAccessToken, async (req, res, next) => {
  try {
    const { indexToDelete } = req.body;
    if (indexToDelete < 0) {
      throw createError.BadRequest('Index cannot be less than 0.');
    }

    const userId = req.payload['aud'];
    const history = await History.findOne({ userId });

    const {
      predictedResult: { classes, probabilities, dates },
    } = history;

    if (!classes || !probabilities || !dates || classes.length - 1 < indexToDelete) {
      return res.status(200).send('OK');
    }

    const predictedResult = { classes: [], probabilities: [], dates: [] };
    for (let i = 0; i < classes.length; i++) {
      if (i === indexToDelete) {
        continue;
      }
      predictedResult.classes.push(classes[i]);
      predictedResult.probabilities.push(probabilities[i]);
      predictedResult.dates.push(dates[i]);
    }

    history.predictedResult = predictedResult;
    const imagesPath = path.join(__dirname, '..', 'users-histories', req.payload.aud);
    fs.rmSync(path.join(imagesPath, `${indexToDelete}.jpg`));
    await history.save();
    return res.status(200).send('OK');
  } catch (err) {
    next(err);
  }
});

router.delete('/clear-history', verifyAccessToken, async (req, res, next) => {
  try {
    const userId = req.payload['aud'];
    await History.findOneAndUpdate({ userId }, { predictedResult: { classes: [], probabilities: [], dates: [] } });
    const imagesPath = path.join(__dirname, '..', 'users-histories', req.payload.aud);
    fs.rmdirSync(imagesPath, { recursive: true });
    return res.status(200).send('OK');
  } catch (err) {
    next(err);
  }
});

module.exports = router;
