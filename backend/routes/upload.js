const express = require('express');
const { verifyAccessToken } = require('../helpers/jwt');
const User = require('../models/User');
const router = express.Router();

router.post('/', verifyAccessToken, async (req, res, next) => {
  console.log(req.headers);
  const user = await User.findById(req.payload.aud);
  res.json(user);
});

module.exports = router;
