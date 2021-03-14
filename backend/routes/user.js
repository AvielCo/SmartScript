const express = require('express');
const router = express.Router();
const User = require('../models/User');
const History = require('../models/History');

router.get('/all', async (req, res) => {
  try {
    const users = await User.find();
    res.status(200).json(users);
  } catch (err) {
    res.json({ message: err });
  }
});

router.post('/add', async (req, res) => {
  const user = {
    email: req.body.email,
    username: req.body.username,
    password: req.body.password,
    name: req.body.name,
  };

  try {
    const newUser = await new User(user).save();
    await new History({ userId: newUser._id }).save();
    res.status(200).json(newUser);
  } catch (err) {
    res.json({ message: err });
  }
});

router.get('/:userId', async (req, res) => {
  try {
    const user = await User.findById(req.params.userId);
    res.status(200).json(user);
  } catch (err) {
    res.json({ message: err });
  }
});

module.exports = router;
