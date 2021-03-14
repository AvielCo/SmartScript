const express = require('express');
const mongoose = require('mongoose');

const app = express();
app.use(express.urlencoded({ extended: true }));
app.use(express.json());

//MongoDB
const uri = 'mongodb://localhost:27017/smartscript-db';
mongoose
  .connect(uri, { useNewUrlParser: true, useUnifiedTopology: true, useFindAndModify: false })
  .then(() => {
    console.log('Connected to db');
  })
  .catch((err) => {
    console.log(err);
  });

//Routes
const uploadRoute = require('./routes/upload');
app.use('/upload', uploadRoute);

const userRoute = require('./routes/user');
app.use('/user', userRoute);

const historyRoute = require('./routes/history');
app.use('/history', historyRoute);

app.listen(3000);
