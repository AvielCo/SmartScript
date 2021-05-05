const express = require("express");
const cors = require("cors");
const morgan = require("morgan");
const createError = require("http-errors");
const history = require("connect-history-api-fallback");
const { createServer } = require("../../helpers/https");
require("dotenv").config();
require("../../helpers/mongodb");

const PORT = process.env.PORT || 8080;

//* Middlewares
const app = express();
app.use(cors());
app.use(history());
app.use(morgan("dev"));
app.use(express.urlencoded({ extended: true }));
app.use(express.json());

//* Routes

//* Upload image routes
app.use("/api/images", require("./routes/images"));

//* Authentication routes
app.use("/api/auth", require("./routes/auth"));

app.use("/api/profile", require("./routes/profile"));

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

//* Nodejs listen to PORT
createServer(app).listen(PORT, () => console.log(`Running on ${PORT}`));
