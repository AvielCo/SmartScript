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

  const third_result = result.success && {
    shape: result.top_results_shape[1][0],
    probability: result.top_results_shape[1][1],
  };

  return (
    <div>
      <div className="results">
        {result.success && (
          <>
            <div className="results-text-view">
              <Paragraph className="results-text result">
                <u>Top result:</u>
                {` ${top_result.origin}-${top_result.shape} `} {top_result.probability}%
              </Paragraph>
              <Paragraph className="results-text result">
                <u>Second result:</u>
                {` ${second_result.origin}-${second_result.shape} `} {second_result.probability}%
              </Paragraph>
              <Paragraph className="results-text result">
                <u>Third result:</u>
                {` ${third_result.shape} `} {third_result.probability}%
              </Paragraph>
            </div>
            <Paragraph strong underline>
              {saved ? "Added to your history, check your profile." : reason}
            </Paragraph>
          </>
        )}
      </div>
    </div>
  );
};
export default ResultTextView;
