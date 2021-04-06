import React, { useState, useEffect } from 'react';

import './List.css';
function CustomList({ data }) {
  const dataList = data.map((single) => {
    return (
      <React.Fragment>
        <div className='list-item'>
          <div className='item-meta'>
            <div className='title'>{`${single.class} - ${single.probability}`}</div>
            <div className='desc'>{<h6 className='item-date'>{single.date}</h6>}</div>
          </div>
          <img className='img' style={{ width: '100px', height: '100px' }} className='item-img' src={single.img} alt='some image' />
        </div>
      </React.Fragment>
    );
  });
  return <div className='theallfather'>{dataList}</div>;
}

export default CustomList;
