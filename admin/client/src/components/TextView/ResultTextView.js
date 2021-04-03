import { Typography, Space } from 'antd';
import React from 'react';
import './ResultTextView.css';

const ResultTextView = ({ result }) => {
  const { Text, Paragraph } = Typography;
  return (
    <div>
      <div className="results">
        {result.success ? (
          <div className="results-text-view">
            <Paragraph>
              <Text type="danger" ellipsis strong>
                {`${result.origin}-${result.shape} `}
              </Text>
              <Text type="danger" ellipsis strong>
                {result.probability}
              </Text>
            </Paragraph>
          </div>
        ) : (
          <Text type="success" ellipsis strong>
            Upload an image and click on predict to see results!
          </Text>
        )}
      </div>
      {result.success && (
        <Paragraph type="danger" strong>
          Added to your history, check your profile.
        </Paragraph>
      )}
    </div>
  );
};
export default ResultTextView;
