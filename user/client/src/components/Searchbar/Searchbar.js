import React, { useState } from 'react';
import { Select, Tag } from 'antd';
import Button from '../Buttons/InputButton';

import './Searchbar.css';

const { Option } = Select;

function Searchbar({ setQuery }) {
  const [shape, setShape] = useState([]);
  const [origin, setOrigin] = useState([]);

  const cartesianProduct = (...arr) => {
    if (arr[0].length === 0 && arr[1].length === 0) {
      // if user click search with both empty fields
      return { searchBy: [], searchType: 'none' };
    } else if (arr[0].length === 0 && arr[1].length !== 0) {
      // if user search by shape only
      return { searchBy: arr[1], searchType: 'shape' };
    } else if (arr[1].length === 0 && arr[0].length !== 0) {
      // if user search by origin only
      return { searchBy: arr[0], searchType: 'origin' };
    }
    // if user search by both shape and origin
    const searchBy = arr.reduce(
      (acc, val) => {
        return acc
          .map((el) => {
            return val.map((element) => {
              return el.concat([element]);
            });
          })
          .reduce((acc, val) => acc.concat(val), []);
      },
      [[]]
    );
    return { searchBy, searchType: 'both' };
  };

  const search = () => {
    const cartesianResult = cartesianProduct(origin, shape);
    if (cartesianResult.searchType === 'both') {
      // if user search by both, combine.
      cartesianResult.searchBy = cartesianResult.searchBy.map((element) => {
        return element.join(' ');
      });
    }
    setQuery(cartesianResult);
  };

  const originOptions = [
    { value: 'ashkenazi', display: 'Ashkenazi' },
    { value: 'byzantine', display: 'Byzantine' },
    { value: 'italian', display: 'Italian' },
    { value: 'oriental', display: 'Oriental' },
    { value: 'sephardic', display: 'Sephardic' },
    { value: 'yemenite', display: 'Yemenite' },
  ];

  const shapeOptions = [
    { value: 'cursive', display: 'Cursive' },
    { value: 'semi_square', display: 'Semi Square' },
    { value: 'square', display: 'Square' },
  ];

  const selectOptions = [
    { onChange: (value) => setOrigin(value), placeholder: 'Origin', options: originOptions },
    { onChange: (value) => setShape(value), placeholder: 'Shape', options: shapeOptions },
  ];

  return (
    <div className="search-container">
      {selectOptions.map((select) => (
        <Select className="select-tags" mode="tags" onChange={select.onChange} placeholder={select.placeholder}>
          {select.options.map((option, i) => (
            <Option key={i} value={option.value}>
              {option.display}
            </Option>
          ))}
        </Select>
      ))}
      <Button onClick={search} name="Search" />
    </div>
  );
}

export default Searchbar;
