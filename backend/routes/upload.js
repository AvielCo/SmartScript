const express = require('express');
const router = express.Router();

router.post('/upload', (req, res) => {
  res.send('upload');
});

module.exports = router;
