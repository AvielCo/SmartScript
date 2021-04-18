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
      predictedResult: { classes, dates, probabilities, images },
    } = await History.findById(user.historyId);

    if (!classes || !probabilities || !dates || !images) {
      return res.send(userData);
    }

    const imagesPath = path.join(__dirname, '..', 'users-histories', req.payload.aud);
    for (let i = 0; i < classes.length; i++) {
      const imageContent = fs.readFileSync(path.join(imagesPath, `${images[i]}.jpg`), 'base64');
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

router.delete('/delete-event/:index', verifyAccessToken, async (req, res, next) => {
  try {
    let { index } = req.params;
    index = parseInt(index);

    if (index < 0) {
      throw createError.BadRequest('Index cannot be less than 0.');
    }

    const userId = req.payload['aud'];
    const history = await History.findOne({ userId });

    const {
      predictedResult: { classes, probabilities, dates, images },
    } = history;

    if (!classes || !probabilities || !dates || !images || classes.length - 1 < index) {
      return res.status(200).send('OK');
    }

    const predictedResult = { classes: [], probabilities: [], dates: [], images: [] };
    let imageToDeletePath = '';
    for (let i = 0; i < classes.length; i++) {
      if (i === index) {
        imageToDeletePath = path.join(__dirname, '..', 'users-histories', req.payload.aud, `${images[i]}.jpg`);
        continue;
      }

      predictedResult.classes.push(classes[i]);
      predictedResult.probabilities.push(probabilities[i]);
      predictedResult.dates.push(dates[i]);
      predictedResult.images.push(images[i]);
    }

    history.predictedResult = predictedResult;
    await history.save();

    // remove the image
    fs.rm(imageToDeletePath, (err) => {
      if (err) {
        console.log(err);
      }
    });

    return res.status(200).send('OK');
  } catch (err) {
    console.log(err);
    next(err);
  }
});

router.delete('/clear-history', verifyAccessToken, async (req, res, next) => {
  try {
    const userId = req.payload['aud'];
    await History.findOneAndUpdate({ userId }, { predictedResult: { classes: [], probabilities: [], dates: [], images: [] } });
    const imagesPath = path.join(__dirname, '..', 'users-histories', req.payload.aud);
    fs.rmdirSync(imagesPath, { recursive: true });
    return res.status(200).send('OK');
  } catch (err) {
    next(err);
  }
});

module.exports = router;
