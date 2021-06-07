import { Typography } from "antd";
import React from "react";
import "./ResultTextView.css";

const ResultTextView = ({ result, savedToHistory: { saved, reason } }) => {
  const { Paragraph } = Typography;

  const top_result = result.success && {
    shape: result.top_results_shape[0][0],
    origin: result.top_results_origin[0][0],
    probability: result.top_results_origin[0][1],
  };

  const second_result = result.success && {
    shape: result.top_results_shape[0][0],
    origin: result.top_results_origin[1][0],
    probability: result.top_results_origin[1][1],
  };

  return (
    <div>
      <div className="results">
        {result.success && (
          <>
            <div className="results-text-view">
              <ol>
                <li>
                  <p className="results-text result top">{`Top prediction result: ${top_result.origin}-${top_result.shape} ${top_result.probability}%`}</p>
                </li>
                <li>
                  <p className="results-text result second">{`Possible second prediction: ${second_result.origin}-${second_result.shape} ${second_result.probability}%`}</p>
                </li>
              </ol>
            </div>
            <p>
              <u>{saved ? "Added to your history, check your profile." : reason}</u>
            </p>
          </>
        )}
      </div>
    </div>
  );
};
export default ResultTextView;
