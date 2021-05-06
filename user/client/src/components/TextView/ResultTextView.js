import { Typography } from "antd";
import React from "react";
import "./ResultTextView.css";

const ResultTextView = ({ result, savedToHistory: { saved, reason } }) => {
  const { Paragraph } = Typography;
  return (
    <div>
      <div className="results">
        {result.success && (
          <>
            <div className="results-text-view">
              <Paragraph className="results-text" underline>
                Results:
              </Paragraph>
              <Paragraph className="results-text result">
                {`${result.origin}-${result.shape} `} {result.probability}%
              </Paragraph>
            </div>
            <Paragraph strong underline>
              {saved ? "Added to your history, check your profile." : reson}
            </Paragraph>
          </>
        )}
      </div>
    </div>
  );
};
export default ResultTextView;
