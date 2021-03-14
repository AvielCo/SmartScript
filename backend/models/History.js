const mongoose = require('mongoose');

const reqArray = {
  type: Array,
  required: true,
};

const ResultSchema = mongoose.Schema({
  class: reqArray,
  probability: reqArray,
});

const PredictSchema = mongoose.Schema({
  images: reqArray,
  results: {
    type: ResultSchema,
    required: true,
  },
});

const HistorySchema = mongoose.Schema({
  userId: {
    type: String,
    required: true,
  },
  predictedResult: {
    type: PredictSchema,
    required: true,
  },
});

module.exports = mongoose.model('History', HistorySchema);
