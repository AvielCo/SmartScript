const mongoose = require('mongoose');
const bcrypt = require('bcrypt');

const reqString = {
  type: String,
  required: true,
};

const reqHideString = {
  ...reqString,
  select: false,
};

const reqLowString = {
  ...reqString,
  lowercase: true,
};

const reqLowUniqueString = {
  ...reqLowString,
  unique: true,
};

const UserSchema = mongoose.Schema({
  email: reqLowUniqueString,
  username: reqLowUniqueString,
  password: reqHideString,
  name: reqString,
});

UserSchema.pre('save', async function (next) {
  try {
    const salt = await bcrypt.genSalt(10);
    const hashedPassword = await bcrypt.hash(this.password, salt);
    this.password = hashedPassword;
    next();
  } catch (err) {
    next(err);
  }
});

module.exports = mongoose.model('User', UserSchema);
