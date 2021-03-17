const mongoose = require('mongoose');

const ResultSchema = mongoose.Schema({
  class: [String],
  probability: [String],
  _id: false,
});

const PredictSchema = mongoose.Schema({
  images: [String],
  results: ResultSchema,
  _id: false,
});

const HistorySchema = mongoose.Schema({
  userId: {
    type: String,
    required: true,
    unique: true,
  },
  predictedResult: PredictSchema,
});

module.exports = mongoose.model('History', HistorySchema);
