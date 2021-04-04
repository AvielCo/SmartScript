import React, {useEffect, useState} from 'react';
import "antd/dist/antd.css";
import "./Home.css";
import { Table, Space } from "antd";
import { InputButton } from "../../components/Buttons";
import axios from 'axios';

function Home (){

    const [data,setData] = useState([{}]);

    const columns = [
        {
            title: "Name",
            dataIndex: "name",
            key: "name",
        },
        {
            title: "Banned",
            dataIndex: " banned",
            key: "banned",
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


    useEffect(() =>{
        axios.get("http://localhost:8080/api/actions/get-all-users")
        .then((res)=>{
                const users = res.data;
                let i = 0; 
                users.forEach((user) =>{
                    user={...user,'key':i}
                    i++
                    console.log(user)
                })
                setData(users);

            }
        ).catch((err)=>{
            console.log(err)})
    },[])



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
