import { List, Avatar, Button, Skeleton, Card } from 'antd';
import React, { useState, useEffect } from 'react';
import staticImage from '../../assets/2.jpg';

import './List.css';
function CustomList({data}) {
  const hardCodeData = [
    { img: staticImage, class: 'Ashkenazi cursive', probability: '99%', date: new Date().toLocaleDateString('he') },
    { img: staticImage, class: 'Sephardic square', probability: '98%', date: new Date().toLocaleDateString('he') },
    { img: staticImage, class: 'Byzantine semi square', probability: '97%', date: new Date().toLocaleDateString('he') },
    { img: staticImage, class: 'Byzantine semi square', probability: '97%', date: new Date().toLocaleDateString('he') },
    { img: staticImage, class: 'Byzantine semi square', probability: '97%', date: new Date().toLocaleDateString('he') },
    { img: staticImage, class: 'Byzantine semi square', probability: '97%', date: new Date().toLocaleDateString('he') },
    { img: staticImage, class: 'Byzantine semi square', probability: '97%', date: new Date().toLocaleDateString('he') },
  ];

  return (
    <div>
      <List
        className='theallfather'
        itemLayout='horizontal'
        dataSource={hardCodeData}
        renderItem={(item) => (
          <List.Item className='list-item' extra={<img className='img' style={{ width: '100px', height: '100px' }} className='item-img' src={item.img} alt='some image' />}>
            <List.Item.Meta className='item-meta' title={`${item.class} - ${item.probability}`} description={<h6 className='item-date'>{item.date}</h6>} />
          </List.Item>
        )}
      />
    </div>
  );
}

export default CustomList;
