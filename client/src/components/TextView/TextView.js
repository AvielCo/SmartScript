import React from 'react';
import './TextView.css';


const TextView =({result})=>{
    return (
      <textarea
        className="results"
        placeholder={result}
        disabled={true}
      />
    );
}
export default TextView;
