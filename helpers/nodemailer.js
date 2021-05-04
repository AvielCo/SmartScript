const nodemailer = require("nodemailer");
require("dotenv").config();

const transport = nodemailer.createTransport({
  service: "Gmail",
  auth: {
    user: process.env.EMAIL_USERNAME,
    pass: process.env.EMAIL_PASSWORD,
  },
});

const sendCredentialEmail = (name, username, password, email) => {
  transport
    .sendMail({
      from: process.env.EMAIL_USERNAME,
      to: email,
      subject: `Thanks ${name} for sign up to SmartScript`,
      html: `<h1>Hello ${name}</h1>
            <h3>Thank you for signin up to SmartScript.</h3>
            <p>Username: ${username} </p>
            <p>Password: ${password} </p>
            <p></p>
            <p>Save this email!</p>`,
    })
    .catch((err) => console.log(err));
};

module.exports = { sendCredentialEmail };
