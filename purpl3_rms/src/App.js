import logo from './res/logo.png';
import './App.css';
import axios from "axios";
import React, {useState} from 'react';
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
import Computer from './pages/Computer'
import PrivateRoute from './components/PrivateRoute'

function App() {

  const [loggedIn, setLogin] = useState(false);

  return (
    <div className="App">
      
      <HashRouter>
        <Switch>
          <Route exact path="/" render={(props) => (<Login {...props} sendLoginStatus={getLoginStatus} />)}/>
          <>
            <div className="logoHeader">
              <img src={logo}/>
            </div>
            <div className="header">
              <button className="logout-button" onClick={handleLogout}/>
              <h1>User stuff goes here</h1>
            </div>
            <ul className="navTabs">
              <li className="tab"><NavLink exact to="/run-script">Run Script</NavLink></li>
              <li className="tab"><NavLink to="/script-logs">Script Logs</NavLink></li>
              <li className="tab"><NavLink to="/schedule">Schedule</NavLink></li>
              <li className="tab"><NavLink to="/script-viewer">Script Viewer</NavLink></li>
              <li className="tab"><NavLink to="/computer">Computer</NavLink></li>
              <li className="tab"><NavLink to="/error-doc">Error Doc</NavLink></li>
            </ul>
            
            <div className="content">
              <PrivateRoute path="/run-script" loginState={loggedIn} component={RunScripts}/>
              <PrivateRoute path="/script-logs" loginState={loggedIn} component={ScriptLogs}/>
              <PrivateRoute path="/schedule" loginState={loggedIn} component={Schedule}/>
              <PrivateRoute path="/script-viewer" loginState={loggedIn} component={ScriptsViewer}/>
              <PrivateRoute path="/computer" loginState={loggedIn} component={Computer}/>
              <PrivateRoute path="/error-doc" loginState={loggedIn} component={ErrorDoc}/>
            </div>
          </>
        </Switch>
      </HashRouter>

      
    </div>
  );

  function getLoginStatus(loginState){
    setLogin(loginState)
  }

  function handleLogout(){
      axios.post("/login", {
        body: {
            op: "LOGOUT",
            data: {
            }
        }
      })
      
    setLogin(false);
  }
}

export default App;
