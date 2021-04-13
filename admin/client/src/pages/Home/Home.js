import React, { useEffect, useState } from 'react';
import 'antd/dist/antd.css';
import './Home.css';
import { Table, Space } from 'antd';
import axios from 'axios';
import greenCircle from '../../assets/green-circle.svg';
import redCircle from '../../assets/red-circle.svg';
import sun from '../../assets/icon-sun.png'
import moon from "../../assets/icon-moon.png";

import {PieChart} from '../../components';


function Home() {
  const [data, setData] = useState([{}]);
  const [updatedField, setUpdatedField] = useState(true);
  const [totalusers, setTotalUsers] = useState(0);
  const [blockedUsers,setBlockedUsers] = useState(0);
  const [time, setTime] = useState(new Date().getTime());
  const [greetingMsg, setGreetingMsg] = useState(" ");
  const [weather,setWeather] = useState(" ");
  const title = "Welcome To SmartScript`s Admin Panel";

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
        setData(res.data);
        setTotalUsers(res.data.length)
        let sum = 0;
        res.data.map((d) => (d.banned && (sum++)));
        setBlockedUsers(sum);
      })
      .catch((err) => {
        console.log(err);
      });
    setUpdatedField(false);
  }, [updatedField]);


  const getGreetingMsg=(hour)=>{
    const greetings={
      morningMsg:'Good Morning',
      noonMsg:'Good Afternoon',
      eveMsg:'Good Evening'
    }

    if(hour>=6 && hour<12){
      setGreetingMsg(greetings.morningMsg);
      setWeather(<img src={sun} alt='sun'/>);
    }
    else if (hour >= 12 && hour < 19) {
      setGreetingMsg(greetings.noonMsg);
      setWeather(<img className="weather-icon" src={sun} alt="sun" />);
    }
    else {
      setGreetingMsg(greetings.eveMsg);
      setWeather(<img className="weather-icon" src={moon} alt="moon" />);
    }

  }

  const getCurrentTime = () => {
    const today = new Date();
    const time = today.getHours() + ":" + today.getMinutes();
    setTime(time);
    getGreetingMsg(today.getHours());
  }

  useEffect(() => {
    getCurrentTime();
  })


  const chartData = [
    {
      label: "Unblocked Users",
      y: totalusers - blockedUsers,
      p: ((totalusers - blockedUsers) / totalusers) * 100,
    },
    {
      label: "Blocked Users",
      y: blockedUsers,
      p: ((blockedUsers) / totalusers) * 100,
    },
  ];

  
  return (
    <div className="home-holder">
      <div className="home-title">
        <div className="weather-time">
          {weather}
          <h5>{time}</h5>
        </div>
        <div className="greeting">
          <h2>{title}</h2>
          <h3>{greetingMsg}</h3>
        </div>
      </div>
      <div className="info">
        <div className="users-table-container">
          <Table
            rowKey={(record) => record._id}
            columns={usersColumns}
            dataSource={data}
            expandable={{
              expandedRowRender: (record) => (
                <Table
                  columns={historyColumns}
                  dataSource={record.history}
                  pagination={false}
                />
              ),
              rowExpandable: (record) => record.history,
            }}
          />
        </div>
        <div className="stats-container">
          <PieChart text={"User Statistics"} dataPoints={chartData} />
        </div>
      </div>
    </div>
  );
}

export default Home;
