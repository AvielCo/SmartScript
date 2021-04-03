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

const AdminSchema = mongoose.Schema({
  username: reqLowUniqueString,
  password: reqHideString,
  name: reqString,
});

//Check if password is equal to hashed password.
AdminSchema.methods.isValidPassword = async function (password) {
  try {
    return await bcrypt.compare(password, this.password);
  } catch (err) {
    console.log(err);
    throw err;
  }
};

module.exports = mongoose.model('Admin', AdminSchema);
