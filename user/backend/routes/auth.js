const express = require("express");
const router = express.Router();
const User = require("../../../models/User");
const History = require("../../../models/History");
const createError = require("http-errors");
const authSchema = require("../validations/auth");
const { decryptStrings } = require("../../../helpers/crypto");
const { signAccessToken, verifyAccessToken } = require("../../../helpers/jwt");
const redis = require("../../../helpers/redis");
const { sendCredentialEmail } = require("../../../helpers/nodemailer");
require("dotenv").config();

router.post("/register", async (req, res, next) => {
  try {
    const { email, username, password, name } = decryptStrings({ email: req.body.email }, { username: req.body.username }, { password: req.body.password }, { name: req.body.name });
    if (!email || !username || !password || !name) {
      throw createError.BadRequest();
    }
    await authSchema.validateAsync({ email, username, password, name });

    const newUserDetails = {
      email,
      username,
      password,
      name,
    };

    //* Check if user exists
    const userExists = await User.findOne({
      $or: [{ email: newUserDetails.email }, { username: newUserDetails.username }],
    });

    if (userExists) {
      //! User is exists
      //! Check which fields are the same and throw an error
      if (userExists.username === newUserDetails.username) {
        throw createError.Conflict("Username is already in use.");
      }
      if (userExists.email === newUserDetails.email) {
        throw createError.Conflict("Email is already in use.");
      }
      throw createError.Conflict();
    }

    //* User is not exists with the same email or username
    const newUser = await new User(newUserDetails).save();
    const history = await new History({ userId: newUser._id, predictedResult: { classes: [], probabilities: [], dates: [] } }).save();
    await User.findByIdAndUpdate(newUser._id, { historyId: history._id });

    sendCredentialEmail(name, username, password, email);

    res.sendStatus(200);
  } catch (err) {
    if (err.isJoi) {
      err.status = 422;
    }
    console.log(err);
    next(err);
  }
});

router.post("/login", async (req, res, next) => {
  try {
    const { username, password } = decryptStrings({ username: req.body.username }, { password: req.body.password });
    const user = await User.findOne({ username }).select("+password");

    if (!user) {
      throw createError.Unauthorized("Username or password are incorrect.");
    }

    const isMatch = await user.isValidPassword(password);
    if (!isMatch) {
      throw createError.Unauthorized("Username or password are incorrect.");
    }

    const accessToken = await signAccessToken(user.id);

    res.status(200).json({ accessToken });
  } catch (err) {
    if (err.isJoi) {
      return next(createError.Unauthorized("Username or password are incorrect."));
    }
    next(err);
  }
});

router.get("/", verifyAccessToken, async (req, res, next) => {
  try {
    const userId = req.payload["aud"];
    return res.sendStatus(200);
  } catch (err) {
    console.log(err);
    next(err);
  }
});

router.delete("/", verifyAccessToken, async (req, res, next) => {
  try {
    const userId = req.payload["aud"];
    redis.DEL(userId, (error, reply) => {
      if (error) {
        throw createError.InternalServerError();
      }
      res.sendStatus(204);
    });
  } catch (error) {
    next(error);
  }
});
module.exports = router;
