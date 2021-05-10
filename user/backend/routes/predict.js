const express = require("express");
const createError = require("http-errors");
const { verifyAccessToken } = require("../../../helpers/jwt");
const User = require("../../../models/User");
const History = require("../../../models/History");
const router = express.Router();
const exec = require("child_process").exec;
const path = require("path");
const uploadFile = require("../../../helpers/upload");
const fs = require("fs");
const sharp = require("sharp");

const insertNewHistory = async (userHistory, newHistory, imageName) => {
  let { predictedResult } = userHistory;
  if (!predictedResult) {
    predictedResult = { classes: [], probabilities: [], dates: [], images: [] };
  }
  predictedResult.classes.push(`${newHistory.origin} ${newHistory.shape}`);
  predictedResult.probabilities.push(newHistory.probability);
  predictedResult.dates.push(new Date());
  predictedResult.images.push(imageName);
  await History.findByIdAndUpdate({ _id: userHistory._id }, { predictedResult });
};

const predict = (data, req, res, next) => {
  const {
    fileDetails: { fileName },
    isUser,
    user,
  } = data;
  const pythonScript = "predict.py";
  const pythonScriptPath = path.join(__dirname, "..", "py-files", pythonScript);
  const pythonScriptCommand = `python ${pythonScriptPath} ${fileName}`;
  const envName = "py36";
  const condaCommand = `conda run -n ${envName}`;
  const child = exec(`${condaCommand} ${pythonScriptCommand}`);

  child.stdout.once("data", async (data) => {
    // message is the response from python script
    let message = JSON.parse(data);
    message = { ...message, savedToHistory: true };
    if (message.success) {
      /**
       * message: {
       *  success: True,
       *  origin: One of the following: "ashkenazi", "bizantine" .....
       *  shape: One of the following: "cursive", "square", "semi-square"
       *  probability: the probability of the prediction
       * }
       */
      try {
        const basePath = path.join(__dirname, "..", "python-folders", "predict-files", "predict-images");
        let filePath = "";
        if (isUser) {
          filePath = path.join(basePath, `${user._id}`, `${fileName}`);
          const userHistory = await History.findById(user.historyId);
          if (!userHistory) {
            fs.rmSync(filePath);
            message = { ...message, savedToHistory: false, reason: "Could not save this image to history. try again later." };
            return res.status(200).send(message);
          }
          // path to save the resized image to view later in the user profile
          const savePath = path.join(__dirname, "..", "users-histories", `${user._id}`);

          fs.mkdir(savePath, { recursive: true }, (err) => {
            if (err) throw createError.InternalServerError();
          });
          sharp(filePath) // resize the image to width: 250px (height is auto scale)
            .resize(250)
            .toFile(path.join(savePath, `${fileName}`))
            .then(() => fs.rmSync(filePath))
            .catch((err) => {
              if (err) {
                message = { ...message, savedToHistory: false, reason: "Could not save this image to history. try again later." };
                return res.status(200).send(message);
              }
            });
          await insertNewHistory(userHistory, message, fileName.split(".")[0]);
        } else {
          message = { ...message, savedToHistory: false, reason: "Log in to write the predictions to history." };
          filePath = path.join(basePath, "guests", `${fileName}`);
        }
        fs.rmSync(filePath);
        return res.status(200).send(message);
      } catch (err) {
        return next(createError.InternalServerError());
      }
    }
    /**
     * message: {
     *  success: False,
     * `reason: Reason that the script failed
     * }
     */
    return next(createError.BadRequest());
  });

  child.stderr.once("data", (data) => {
    console.log(data);
  });

  child.once("error", function (err) {
    console.log(err);
    throw next(createError.InternalServerError());
  });
};

router.post("/", verifyAccessToken, async (req, res, next) => {
  try {
    await uploadFile(req, res)
      .then(async () => {
        const fileName = req.file.filename;
        let data = {
          fileDetails: { fileName },
        };
        if (req.payload && req.payload.aud) {
          const user = await User.findById(req.payload.aud);
          data = {
            ...data,
            isUser: true,
            user,
          };
        } else {
          data = {
            ...data,
            isUser: false,
          };
        }
        predict(data, req, res, next);
      })
      .catch((err) => {
        console.log(err);
        throw createError.BadRequest("Not uploaded");
      });
  } catch (err) {
    console.log(err);
    next(err);
  }
});

module.exports = router;
