import { Typography } from "antd";
import React from "react";
import "./ResultTextView.css";

const ResultTextView = ({ result, savedToHistory: { saved, reason } }) => {
  const { Text, Paragraph } = Typography;
  return (
    <div>
      <div className="results">
        {result.success ? (
          <div className="results-text-view">
            <Paragraph className="results-text">
              {`${result.origin}-${result.shape} `} {result.probability}%
            </Paragraph>
          </div>
        ) : (
          <Text ellipsis strong>
            Upload an image and click on predict to see results!
          </Text>
        )}
      </div>
      {result.success && saved ? <Paragraph strong>Added to your history, check your profile.</Paragraph> : result.success && <Paragraph strong>{reason}</Paragraph>}
    </div>
  );
};
export default ResultTextView;
