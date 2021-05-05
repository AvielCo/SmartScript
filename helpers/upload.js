const util = require("util");
const multer = require("multer");
const path = require("path");
const fs = require("fs");
const { genRandomString } = require("../helpers/helpers");

const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    const basePath = path.join(__dirname, "..", "user", "backend", "python-folders", "predict-files", "predict-images");
    const uploadPath = req.payload && req.payload.aud ? path.join(basePath, req.payload.aud) : path.join(basePath, "guests");
    fs.mkdir(uploadPath, (err) => {
      if (err && req.payload && req.payload.aud) {
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
}).single("file");

const uploadFileMW = util.promisify(uploadFile);

module.exports = uploadFileMW;
