const mongoose = require('mongoose');

const defArray = {
  type: Array,
  default: [],
};

const ResultSchema = mongoose.Schema({
  class: defArray,
  probability: defArray,
});

const PredictSchema = mongoose.Schema({
  images: defArray,
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
