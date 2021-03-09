import React from 'react';
import './TextView.css';


const TextView =({result})=>{
    return (
      <textarea className="results" placeholder="Result"  disabled={true}>{result}</textarea>
    );
}
export default TextView;
