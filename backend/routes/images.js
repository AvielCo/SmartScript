const express = require('express');
const createError = require('http-errors');
const { verifyAccessToken } = require('../helpers/jwt');
const User = require('../models/User');
const router = express.Router();
const exec = require('child_process').exec;

router.post('/upload', verifyAccessToken, async (req, res, next) => {
  try {
    await User.findOneAndUpdate({ _id: req.payload.aud }, { imageToScan: req.body.image });
    return res.status(200).send('Image uploaded successfully.');
  } catch (err) {
    next(err);
  }
});

router.post('/scan', verifyAccessToken, async (req, res, next) => {
  try {
    const user = await User.findOne({ _id: req.payload.aud });
    let imageToScan = user.imageToScan;

    const pythonScript = 'decoder.py';
    const envName = 'py36';

    const child = exec(`conda activate ${envName} && python ${__dirname}\\${pythonScript}`);
    child.stdin.write(imageToScan);
    child.stdin.end();

    child.stdout.on('data', function (data) {
      return res.status(200).json(data);
    });

    child.stderr.on('data', function (data) {
      console.log('stdout: ' + data);
    });

    child.on('close', function (code) {
      console.log('closing code: ' + code);
    });

    child.on('error', function (err) {
      console.log(err);
    });
  } catch (err) {
    console.log(err);
    next(err);
  }
});

module.exports = router;
