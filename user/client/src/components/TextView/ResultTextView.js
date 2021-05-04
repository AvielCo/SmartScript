import { Typography } from 'antd';
import React from 'react';
import './ResultTextView.css';

const ResultTextView = ({ result }) => {
  const { Text, Paragraph } = Typography;
  return (
    <div>
      <div className='results'>
        {result.success && (
          <div className='results-text-view'>
            <Paragraph className='results-text'>
              {`${result.origin}-${result.shape} `} {result.probability}%
            </Paragraph>
          </div>
        )}
      </div>
      {result.success && <Paragraph strong>Added to your history, check your profile.</Paragraph>}
    </div>
  );
};
export default ResultTextView;
