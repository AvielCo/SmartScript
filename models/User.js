const mongoose = require('mongoose');
const bcrypt = require('bcrypt');

const reqString = {
  type: String,
  required: true,
};

const emptyString = {
  type: String,
  default: '',
  required: false,
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
  historyId: emptyString,
  imageToScan: emptyString,
});

//Check if password is equal to hashed password.
UserSchema.methods.isValidPassword = async function (password) {
  try {
    return await bcrypt.compare(password, this.password);
  } catch (err) {
    console.log(err);
    throw err;
  }
};

//When save() is fired
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
