const mongoose = require('mongoose');
require('dotenv').config();

// * Get the secret uri from dotenv
const uri = process.env.MONGODB_URI;

//* Connect to MongoDB
mongoose
  .connect(uri, {
    dbName: process.env.SMARTSCRIPT_DB,
    useNewUrlParser: true,
    useUnifiedTopology: true,
    useFindAndModify: false,
    useCreateIndex: true,
  })
  .then(() => {
    console.log('[MongoDB] Connected to db');
  })
  .catch((err) => {
    console.log(err);
  });

//* Listeners
mongoose.connection.on('connected', () => {
  console.log('[Mongoose] Mongoose successfully connected');
});

mongoose.connection.on('error', (err) => {
  console.log(`[Mongoose] ${err.message}`);
});

mongoose.connection.on('disconnected', () => {
  console.log('[Mongoose] Mongoose connection disconnected');
});

process.on('SIGINT', async () => {
  await mongoose.connection.close();
  process.exit(0);
});
