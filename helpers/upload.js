const util = require('util');
const multer = require('multer');
const path = require('path');
const fs = require('fs');
const { genRandomString } = require('../helpers/helpers');

const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    const uploadPath = path.join(__dirname, '..', 'user', 'backend', 'python-folders', 'predict-files', 'predict_images', req.payload.aud);
    fs.mkdir(uploadPath, (err) => {
      if (err) {
        fs.rmdirSync(uploadPath, { recursive: true });
        fs.mkdirSync(uploadPath, { recursive: true });
      }
      cb(null, uploadPath);
    });
  },
  filename: (req, file, cb) => {
    const imageName = genRandomString(40);
    cb(null, `${imageName}.jpg`);
  },
});

const uploadFile = multer({
  storage: storage,
}).single('file');

const uploadFileMW = util.promisify(uploadFile);

module.exports = uploadFileMW;
