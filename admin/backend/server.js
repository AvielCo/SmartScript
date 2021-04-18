const express = require('express');
const cors = require('cors');
const path = require('path');
const morgan = require('morgan');
const createError = require('http-errors');
const history = require('connect-history-api-fallback');
require('dotenv').config();
require('../../helpers/mongodb');

const PORT = process.env.PORT || 8080;

//* Middlewares
const app = express();
app.use(cors());
app.use(morgan('dev'));
app.use(history());
app.use(express.urlencoded({ extended: true }));
app.use(express.json());
app.use('/', express.static(path.join(__dirname, 'build')));

//* Routes

//* Authentication routes
app.use('/api/auth', require('./routes/auth'));

app.use('/api/actions', require('./routes/actions'));

//! 404 Error handling
app.use(async (req, res, next) => {
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

//* Nodejs listen to PORT
app.listen(PORT, () => console.log(`[node.js] Server running on port ${PORT}`));
