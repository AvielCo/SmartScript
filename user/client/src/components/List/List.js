import React from 'react';
import axios from 'axios';
import './List.css';

function CustomList({ data, query }) {
  const dataList = data
    .filter((single) => {
      const [origin, shape] = single.class.split(' '); // split the class from 'origin shape' to 'origin', 'shape'
      switch (query.searchType) {
        case 'origin': // search by origin
          if (query.searchBy.includes(origin)) return single;
          break;
        case 'shape': // search by shape
          if (query.searchBy.includes(shape)) return single;
          break;
        case 'both': // search by both origin and shape
          if (query.searchBy.includes(`${origin} ${shape}`)) return single;
          break;
        default:
          // user clicked on search with empty request
          return single;
      }
    })
    .map((single, i) => {
      return (
        <React.Fragment>
          <div className="list-item">
            <div className="item-meta">
              <div className="title">{`${single.class} - ${single.probability}`}</div>
              <div className="desc">{<h6 className="item-date">{single.date}</h6>}</div>
            </div>
            <img className="img" style={{ width: '100px', height: '100px' }} className="item-img" src={single.image} alt="some image" />
          </div>
        </React.Fragment>
      );
    });

  return <div className="theallfather">{dataList}</div>;
}

export default CustomList;
