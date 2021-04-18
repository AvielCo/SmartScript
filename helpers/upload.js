const util = require('util');
const multer = require('multer');
const path = require('path');
const fs = require('fs');

const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    const uploadPath = path.join(__dirname, '..', 'user', 'backend', 'python-folders', 'predict-files', 'predict_images', req.payload.aud);
    fs.mkdir(uploadPath, { recursive: true }, (err) => {
      console.log(err);
    });
    cb(null, uploadPath);
  },
  filename: (req, file, cb) => {
    cb(null, 'imageToUpload.jpg');
  },
});

const uploadFile = multer({
  storage: storage,
}).single('file');

const uploadFileMW = util.promisify(uploadFile);

module.exports = uploadFileMW;
