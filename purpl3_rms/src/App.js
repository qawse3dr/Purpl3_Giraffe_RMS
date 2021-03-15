import logo from './logo.svg';
import './App.css';
import axios from "axios";
import React, { Component } from 'react';
import MenuTab from "./components/MenuTab"

function App() {
  return (
    <div className="App">
      
      <button onClick={Ping}>Ping</button>

      <MenuTab/>

      
    </div>
  );
}

function Ping(){
  
  axios.post("/ping", {
    body: {ping:"ping"}
    }).then((res) => {
      alert(JSON.stringify(res.data))
    }).catch((res) =>{
      alert("Post Failed")
    })
}
export default App;
