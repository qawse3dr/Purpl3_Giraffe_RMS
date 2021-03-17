import logo from './res/logo.png';
import './App.css';
import axios from "axios";
import React, { Component, useState } from 'react';
import {
  Route,
  Switch,
  NavLink,
  HashRouter
} from "react-router-dom";
import Login from './pages/Login';
import RunScripts from './pages/RunScript'
import Schedule from './pages/Schedule'
import ScriptLogs from './pages/ScriptLogs'
import ScriptsViewer from './pages/ScriptsViewer'
import ErrorDoc from './pages/ErrorDoc'

function App() {

  return (
    <div className="App">
      
      <HashRouter>
        <div className="logoHeader">
          <img src={logo}></img>
        </div>
        <div className="header">
          <h1>User stuff goes here</h1>
        </div>
        <ul className="navTabs">
          <li className="tab"><NavLink exact to="/run-script">Run Script</NavLink></li>
          <li className="tab"><NavLink to="/script-logs">Script Logs</NavLink></li>
          <li className="tab"><NavLink to="/schedule">Schedule</NavLink></li>
          <li className="tab"><NavLink to="/script-viewer">Script Viewer</NavLink></li>
          <li className="tab"><NavLink to="/error-doc">Error Doc</NavLink></li>
        </ul>
        

        <div className="content">
          <Switch>
            <Route path="/run-script" component={RunScripts}></Route>
            <Route path="/script-logs" component={ScriptLogs}></Route>
            <Route path="/schedule" component={Schedule}></Route>
            <Route path="/script-viewer" component={ScriptsViewer}></Route>
            <Route path="/error-doc" component={ErrorDoc}></Route>
          </Switch>
        </div>
      </HashRouter>

      
    </div>
  );
}

//.getElementsByClassName("tab").onClick = () => {
 // if this.

//}

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
