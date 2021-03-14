const express = require('express');
const router = express.Router();

const History = require('../models/History');

router.get('/all', async (req, res) => {
  try {
    const histories = await History.find();
    res.status(200).json(histories);
  } catch (err) {
    res.json({ message: err });
  }
});

router.post('/add', async (req, res) => {
  const history = {
    userId: req.body.userId,
    predictedResult: req.body.predictedResult,
  };

  try {
    const newHistory = await new History(history).save();
    res.status(200).json(newHistory);
  } catch (err) {
    res.json({ message: err });
  }
});

//TODO: fix route to be beutifullier
router.post('/insert/:userId', async (req, res) => {
  const { predictedResult } = await History.findOne({ userId: req.params.userId });
  predictedResult.images.push(req.body.newImage);
  predictedResult.results.class.push(req.body.newClass);
  predictedResult.results.probability.push(req.body.newProb);
  try {
    const userHistory = await History.findOneAndUpdate({ userId: req.params.userId }, { predictedResult });
    res.status(200).json(userHistory);
  } catch (err) {
    res.json({ message: err });
  }
});

router.get('/:userId', async (req, res) => {
  try {
    const userHistory = await History.findOne({ userId: req.params.userId });
    res.status(200).json(userHistory);
  } catch (err) {
    res.json({ message: err });
  }
});

module.exports = router;
