import React, { useEffect, useState } from 'react';
import 'antd/dist/antd.css';
import './Home.css';
import { Table, Space } from 'antd';
import axios from 'axios';
import greenCircle from '../../assets/green-circle.svg';
import redCircle from '../../assets/red-circle.svg';

function Home() {
  const [data, setData] = useState([{}]);
  const [updatedField, setUpdatedField] = useState(true);

  const usersColumns = [
    { title: 'Name', dataIndex: 'name', key: 'name' },
    { title: 'Username', dataIndex: 'username', key: 'username' },
    { title: 'Email', dataIndex: 'email', key: 'email' },
    { title: 'Banned', dataIndex: 'banned', key: 'banned', render: (banned) => (banned ? <img alt="V" src={redCircle} width="20" /> : <img alt="X" src={greenCircle} width="20" />) },
    {
      title: 'Actions',
      dataIndex: 'actions',
      key: 'actions',
      render: (text, record) => (
        <Space size="middle">
          <a href="#" onClick={(e) => editBanUser(record._id, record.banned, e)}>
            {record.banned ? 'Unblock' : 'Block'}
          </a>
        </Space>
      ),
    },
  ];

  const historyColumns = [
    {
      title: 'Date',
      dataIndex: 'date',
      key: 'date',
      render: (text, record) => {
        return new Date(record.date).toLocaleDateString('he');
      },
    },
    { title: 'Class', dataIndex: 'class', key: 'class' },
    { title: 'Probability', dataIndex: 'probability', key: 'probability' },
  ];

  const editBanUser = (userId, isBanned, event) => {
    event.preventDefault();
    axios
      .post(`http://34.76.66.213:8080/api/actions/${isBanned ? 'un' : ''}ban-user`, { userId })
      .then((res) => {
        setUpdatedField(true);
      })
      .catch((err) => {
        console.log(err);
      });
  };

  useEffect(() => {
    if (!updatedField) {
      return;
    }
    axios
      .get('http://34.76.66.213:8080/api/actions/get-all-users')
      .then((res) => {
        console.log(res.data);
        setData(res.data);
      })
      .catch((err) => {
        console.log(err);
      });
    setUpdatedField(false);
  }, [updatedField]);

  return (
    <div className="home-holder">
      <div>
        <div className="users-table-container">
          <Table
            rowKey={(record) => record._id}
            columns={usersColumns}
            dataSource={data}
            expandable={{
              expandedRowRender: (record) => <Table columns={historyColumns} dataSource={record.history} pagination={false} />,
              rowExpandable: (record) => record.history,
            }}
          />
        </div>
      </div>
    </div>
  );
}

export default Home;
