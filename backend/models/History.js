const mongoose = require('mongoose');

const ResultSchema = mongoose.Schema({
  class: Array,
  probability: Array,
});

const PredictSchema = mongoose.Schema({
  images: Array,
  results: ResultSchema,
});

const HistorySchema = mongoose.Schema({
  userId: {
    type: String,
    required: true,
  },
  predictedResult: PredictSchema,
});

module.exports = mongoose.model('History', HistorySchema);
