const mongoose = require('mongoose');

const PredictSchema = mongoose.Schema({
  classes: [String],
  probabilities: [String],
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
