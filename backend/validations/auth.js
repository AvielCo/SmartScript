const Joi = require('@hapi/joi');

const authSchema = Joi.object({
  email: Joi.string().email().required(),
  username: Joi.string().alphanum().min(3).max(20).required(),
  password: Joi.string().min(6).max(20).required(), //https://github.com/kamronbatman/joi-password-complexity
  name: Joi.string().required(),
});
// .pattern(new RegExp(/^[a-zA-Z]+$/))
module.exports = authSchema;
