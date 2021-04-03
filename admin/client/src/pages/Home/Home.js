import React from 'react';
import "antd/dist/antd.css";
import "./Home.css";
import { Table, Space } from "antd";
import { InputButton } from "../../components/Buttons";
import axios from 'axios';

function Home (){

const columns = [
    {
        title: "Name",
        dataIndex: "name",
        key: "name",
    },
    {
        title: "Title",
        dataIndex: "title",
        key: "title",
    },
    {
        title: "Actions",
        key: "actions",
        render: (text, record) => (
            <Space size="middle">
            <a>Block</a>
            <a>Go To Profile</a>
            </Space>
        ),
    },
];

// componentDidMount=() => {
//     this.fetchData();
// }

// fetchData = () =>{
//     axios.get().
//     than((response) =>{
//         const data = response.data;
//         this.setState(something here);
//         console.log("data had been received");
//     })
//     .catch(()=>{
//         alert("error retrieving data!!!")
//     });
// }

const data = [
  {
    key: "1",
    name: "Aviel Cohen",
    title: "engineer"
  },
  {
    key: "2",
    name: "Noah Solomon",
    title: "engineer"
  },
  {
    key: "3",
    name: "Emilia Zorin",
    title: "engineer"
  },
];

return (
    <div className="home-holder">
        <div className="users-table-container">
            <Table columns={columns} dataSource={data} />
        </div>
        <div className="logout-btn">
            <InputButton name="Logout"></InputButton>
        </div>
    </div>
    )
}

export default Home;
