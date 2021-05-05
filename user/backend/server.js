const express = require('express');
const cors = require('cors');
const morgan = require('morgan');
const createError = require('http-errors');
const history = require('connect-history-api-fallback');
const { createServer } = require('../../helpers/https');
const path = require("path");
require('dotenv').config();
require('../../helpers/mongodb');

const PORT = process.env.PORT || 8080;

//* Middlewares
const app = express();
app.use(cors());
app.use(history());
app.use(morgan('dev'));
app.use(express.urlencoded({ extended: true }));
app.use(express.json());

//* Routes
app.get("/.well-known/pki-validation/FEE6D8CBA78F8BD2D35CDAAF9D93C836.txt", (req, res, next) => {
  res.sendFile(path.join(__dirname, ".well-known", "pki-validation", "FEE6D8CBA78F8BD2D35CDAAF9D93C836.txt"));
});

//* Upload image routes
app.use('/api/images', require('./routes/images'));

//* Authentication routes
app.use('/api/auth', require('./routes/auth'));

app.use('/api/profile', require('./routes/profile'));

//! 404 Error handling
app.use((req, res, next) => {
  next(createError.NotFound());
});

//! Error handling
app.use((err, req, res, next) => {
  res.status(err.status || 500);
  res.send({
    error: {
      status: err.status || 500,
      message: err.message,
    },
  });
});

createServer(app).listen(PORT, () => console.log(`Running on ${PORT}`));
