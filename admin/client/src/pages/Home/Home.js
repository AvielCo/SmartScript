import React, { useEffect, useState } from "react";
import "antd/dist/antd.css";
import "./Home.css";
import { Table, Space } from "antd";
import { ToastContainer, toast } from "react-toastify";
import axios from "axios";
import greenCircle from "../../assets/green-circle.svg";
import redCircle from "../../assets/red-circle.svg";
import sun from "../../assets/icon-sun.png";
import moon from "../../assets/icon-moon.png";
import { getAccessToken, useWindowDimensions } from "../../helpers";
import { Doughnut } from "react-chartjs-2";

import "react-toastify/dist/ReactToastify.css";
import { Redirect } from "react-router";
import { NavBar } from "../../components";

function Home() {
  const [data, setData] = useState([{}]);
  const [updatedField, setUpdatedField] = useState(true);
  const [totalusers, setTotalUsers] = useState(0);
  const [blockedUsers, setBlockedUsers] = useState(0);
  const [time, setTime] = useState(new Date().getTime());
  const [greetingMsg, setGreetingMsg] = useState(" ");
  const [weather, setWeather] = useState(" ");
  const [loading, setLoading] = useState(true);
  const { width } = useWindowDimensions();
  const title = "Welcome To SmartScript`s Admin Panel";

  const deleteTokenFromStorage = () => {
    window.sessionStorage.removeItem("accessToken");
    window.localStorage.removeItem("accessToken");
  };

  const editBanUser = (userId, isBanned, event) => {
    if (loading) return;
    setLoading(true);
    event.preventDefault();

    const cfg = {
      headers: {
        Authorization: "Bearer " + getAccessToken(),
        IsAdmin: true,
      },
    };

    axios
      .post(`http://${process.env.REACT_APP_API_ADDRESS}:8080/api/actions/edit-ban`, { userId, ban: !isBanned }, cfg)
      .then((res) => {
        if (res.status === 200) {
          setUpdatedField(true);
          toast.info(!isBanned ? "Banned Successfully!" : "Unbanned Successfully!");
        }
      })
      .catch((err) => {
        if (err.response) {
          const { status, message } = err.response.data.error;
          if (status === 401) {
            deleteTokenFromStorage();
          } else toast.error(message);
        }
      })
      .finally(() => {
        setLoading(false);
      });
  };

  const getGreetingMsg = (hour) => {
    const greetings = {
      morningMsg: "Good Morning",
      noonMsg: "Good Afternoon",
      eveMsg: "Good Evening",
    };

    if (hour >= 6 && hour < 12) {
      setGreetingMsg(greetings.morningMsg);
      setWeather(<img className="weather-icon" src={sun} alt="sun" />);
    } else if (hour >= 12 && hour < 19) {
      setGreetingMsg(greetings.noonMsg);
      setWeather(<img className="weather-icon" src={sun} alt="sun" />);
    } else {
      setGreetingMsg(greetings.eveMsg);
      setWeather(<img className="weather-icon" src={moon} alt="moon" />);
    }
  };

  const getCurrentTime = () => {
    const today = new Date();
    const minutes = today.getMinutes() >= 10 ? today.getMinutes() : "0" + today.getMinutes();
    const hours = today.getHours() >= 10 ? today.getHours() : "0" + today.getHours();
    const currTime = hours + ":" + minutes;
    if (time !== currTime) {
      setTime(currTime);
      getGreetingMsg(today.getHours());
    }
  };

  useEffect(() => {
    if (!updatedField) {
      return;
    }
    setLoading(true);

    const cfg = {
      headers: {
        Authorization: "Bearer " + getAccessToken(),
        IsAdmin: true,
      },
    };

    axios
      .get(`http://${process.env.REACT_APP_API_ADDRESS}:8080/api/actions/get-all-users`, cfg)
      .then((res) => {
        if (res.status === 200) {
          setData(res.data);
          setTotalUsers(res.data.length);
          let sum = 0;
          res.data.map((d) => d.banned && sum++);
          setBlockedUsers(sum);
        }
      })
      .catch((err) => {
        if (err.response) {
          const { status, message } = err.response.data.error;
          if (status === 401) {
            deleteTokenFromStorage();
            toast.error("Please log in to watch all users.");
          }
          toast.error(message);
        }
      })
      .finally(() => {
        setLoading(false);
      });
    setUpdatedField(false);
  }, [updatedField]);

  useEffect(() => {
    getCurrentTime();
  }, [time]);

  const usersColumns = [
    { title: "Username", dataIndex: "username", key: "username", width: width < 1220 ? "12%" : "17%" },
    { title: "Email", dataIndex: "email", key: "email", width: width < 1220 ? "20%" : "30%" },
    {
      title: "Banned",
      dataIndex: "banned",
      width: width < 1220 ? "7%" : "12%",
      key: "banned",
      render: (banned) => (banned ? <img alt="V" src={redCircle} width="20" /> : <img alt="X" src={greenCircle} width="20" />),
    },
    {
      title: "Actions",
      dataIndex: "actions",
      key: "actions",
      width: width < 1220 ? "6%" : "13%",
      render: (text, record) => (
        <Space size="middle">
          <a href="#" onClick={(e) => editBanUser(record._id, record.banned, e)}>
            {record.banned ? "Unblock" : "Block"}
          </a>
        </Space>
      ),
    },
  ];

  const historyColumns = [
    {
      title: "Date",
      dataIndex: "date",
      key: "date",
      render: (text, record) => {
        return new Date(record.date).toLocaleDateString("he");
      },
    },
    { title: "Class", dataIndex: "class", key: "class" },
    { title: "Probability", dataIndex: "probability", key: "probability" },
  ];

  const chartData = {
    labels: ["Blocked", "Unblocked"],
    datasets: [
      {
        label: "# of Users",
        data: [blockedUsers, totalusers - blockedUsers],
        backgroundColor: ["rgba(255,65,65,0.5)", "rgba(107,190,102,0.5)"],
        borderColor: ["rgba(255,65,65,1)", "rgba(107,190,102,255)"],
        borderWidth: 2,
        hoverOffset: 30,
      },
    ],
  };

  const chartOptions = {
    maintainAspectRatio: true,
    animation: false,
    legend: {
      position: "bottom",
      labels: { fontColor: "#000000", fontSize: 15, fontFamily: "Times New Roman, Times, serif" },
    },
  };

  return (
    <React.Fragment>
      {!getAccessToken() ? (
        <Redirect to="/login" />
      ) : (
        <>
          <ToastContainer position="top-left" autoClose={5000} hideProgressBar={false} newestOnTop closeOnClick rtl={false} pauseOnFocusLoss draggable pauseOnHover />
          <NavBar />
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
                  pagination={false}
                  rowKey={(record) => record._id}
                  scroll={width < 1220 && { x: "calc(700px + 50%)", y: 240 }}
                  loading={loading}
                  columns={usersColumns}
                  dataSource={data}
                  expandable={{
                    expandedRowRender: (record) => <Table columns={historyColumns} dataSource={record.history} pagination={false} />,
                    rowExpandable: (record) => record.history,
                  }}
                />
              </div>
              {data.length > 0 && (
                <div className="chart-container">
                  <Doughnut data={chartData} options={chartOptions} />
                </div>
              )}
            </div>
          </div>
        </>
      )}
    </React.Fragment>
  );
}

export default Home;
