const express = require('express');
const createError = require('http-errors');
const { verifyAccessToken } = require('../helpers/jwt');
const User = require('../models/User');
const History = require('../models/History');
const router = express.Router();
const exec = require('child_process').exec;
const path = require('path');
const uploadFile = require('../helpers/upload');
const fs = require('fs');
const sharp = require('sharp');

const insertNewHistory = async (userHistory, newHistory) => {
  let { predictedResult } = userHistory;
  if (predictedResult === undefined) {
    predictedResult = { classes: [], probabilities: [] };
  }
  predictedResult.classes.push(`${newHistory.origin}-${newHistory.shape}`);
  predictedResult.probabilities.push(newHistory.probability);
  await History.findByIdAndUpdate({ _id: userHistory._id }, { predictedResult });
};

router.post('/upload', verifyAccessToken, async (req, res, next) => {
  try {
    await uploadFile(req, res)
      .then(() => res.status(200).send('Image uploaded successfully.'))
      .catch((err) => {
        throw createError.BadRequest();
      });
  } catch (err) {
    next(err);
  }
});

router.post('/scan', verifyAccessToken, async (req, res, next) => {
  try {
    const user = await User.findOne({ _id: req.payload.aud });

    const pythonScript = 'predict.py';
    const pythonScriptPath = path.join(process.cwd(), 'py-files', pythonScript);
    const pythonScriptCommand = `python ${pythonScriptPath}  ${user._id}`;
    const envName = 'py36';
    const condaCommand = `conda activate ${envName}`;
    const child = exec(`${condaCommand} && ${pythonScriptCommand}`);

    child.stdout.on('data', async function (data) {
      const message = JSON.parse(data);
      if (message.success) {
        let totalImages = 0;
        const imagePath = path.join(process.cwd(), 'python-folders', 'predict-files', 'predict_images', `${user._id}`, 'imageToUpload.jpg');
        const userHistory = await History.findById({ _id: user.historyId });
        if (userHistory.predictedResult) {
          totalImages = userHistory.predictedResult.classes.length;
        }
        const savePath = path.join(process.cwd(), 'users-histories', `${user._id}`);
        fs.mkdir(savePath, { recursive: true }, (err) => {
          if (err) throw createError.BadRequest();
        });
        sharp(imagePath)
          .resize(400)
          .toFile(path.join(savePath, `${totalImages}.jpg`));

        await insertNewHistory(userHistory, message);
        return res.status(200).send(message);
      }
      throw createError.BadRequest();
    });

    child.on('error', function (err) {
      throw next(err);
    });
  } catch (err) {
    console.log(err);
    next(err);
  }
});

module.exports = router;
