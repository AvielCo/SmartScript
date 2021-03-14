const mongoose = require('mongoose');

const reqString = {
  type: String,
  required: true,
};

const UserSchema = mongoose.Schema({
  email: reqString,
  username: reqString,
  password: reqString,
  name: reqString,
});

module.exports = mongoose.model('User', UserSchema);
