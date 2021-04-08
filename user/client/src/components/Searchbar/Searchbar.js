import React, { useState } from 'react';

import { Select } from 'antd';

const { Option, OptGroup } = Select;

function Searchbar({ setQuery }) {
  const [shape, setShape] = useState([]);
  const [origin, setOrigin] = useState([]);

  const chooseOrigin = (value) => {
    setOrigin(value);
  };
  const chooseShape = (value) => {
    setShape(value);
  };

  const cartesianProduct = (...arr) => {
    return arr.reduce(
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
  };

  const search = () => {
    const cartesianResult = cartesianProduct(origin, shape);
    const cartesian = cartesianResult.map((element) => {
      return element.join(' ');
    });
    setQuery(cartesian);
  };
  return (
    <React.Fragment>
      <Select mode='tags' style={{ width: 200 }} onChange={chooseOrigin}>
        <OptGroup label='origin'>
          <Option key={1} value='Ashkenazi'>
            Ashkenazi
          </Option>
          <Option key={2} value='Byzantine'>
            Byzantine
          </Option>
          <Option key={3} value='Italian'>
            Italian
          </Option>
          <Option key={4} value='Oriental'>
            Oriental
          </Option>
          <Option key={5} value='Sephardic'>
            Sephardic
          </Option>
          <Option key={6} value='Yemenite'>
            Yemenite
          </Option>
        </OptGroup>
      </Select>
      <Select mode='tags' style={{ width: 200 }} onChange={chooseShape}>
        <OptGroup label='Shape'>
          <Option key={1} value='cursive'>
            Cursive
          </Option>
          <Option key={2} value='square'>
            Square
          </Option>
          <Option key={3} value='semi-square'>
            Semi-Square
          </Option>
        </OptGroup>
      </Select>
      <button onClick={search}>Search</button>
    </React.Fragment>
  );
}

export default Searchbar;
