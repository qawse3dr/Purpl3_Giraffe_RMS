import logo from './res/logo.png';
import logoutBtn from "./res/logout.png"
import './App.css';
import axios from "axios";
import React, {useState} from 'react';
import {
  Route,
  Switch,
  HashRouter
} from "react-router-dom";
import {Navbar, Nav } from 'react-bootstrap'
import Login from './components/login/Login';
import RunScriptPage from './components/run_script_page/run_script_page';
//import Schedule from 
import ScriptLogPage from './components/script_log/script_log';
// import ScriptsViewer from './pages/ScriptsViewer'
import ScriptViewPage from './components/scriptView_Page/scriptViewer_P';

import ErrorDoc from './components/errorDoc/errorDoc'
import ComputerViewer from './components/computers/computers'
import PrivateRoute from './components/PrivateRoute'
import {LinkContainer} from "react-router-bootstrap"

function App() {

  const [loggedIn, setLogin] = useState(false);

  return (
    <div className="App">
      
      <HashRouter>
        <Switch>
          <Route exact path="/" render={(props) => (<Login {...props} sendLoginStatus={getLoginStatus} />)}/>
          <Route>
            <div className="MenuBar">

              <Navbar bg="dark" expand="lg" variant="dark">
              <Navbar.Toggle aria-controls="responsive-navbar-nav" />
              <Navbar.Brand>
                <img
                  src={logo}
                  height="50"
                  className="d-inline-block align-top"
                  alt="Purpl3 Giraffe logo"
                />
              </Navbar.Brand>
              <Navbar.Collapse id="responsive-navbar-nav"> 
                <Nav className="mr-auto">
                  <LinkContainer to="/run-script">
                    <Nav.Link>
                      Run Script
                    </Nav.Link>
                  </LinkContainer>

                  <LinkContainer to="/script-logs">
                    <Nav.Link>
                      Script Logs
                    </Nav.Link>
                  </LinkContainer>

                  <LinkContainer to="/script-viewer">
                    <Nav.Link>
                      Script Viewer
                    </Nav.Link>
                  </LinkContainer>

                  <LinkContainer to="/computerViewer">
                    <Nav.Link>
                      Computer Viewer
                    </Nav.Link>
                  </LinkContainer>

                  <LinkContainer to="/error-doc">
                    <Nav.Link>
                      Error Doc
                    </Nav.Link>
                  </LinkContainer>       
                </Nav>
              </Navbar.Collapse>

              <img
                  src={logoutBtn}
                  height="50"
                  onClick={handleLogout}
                  className="d-inline-block align-top "
                  alt="Logout logo"
                />

            </Navbar>

            </div>
            <div className="content">
              <Switch>
                <PrivateRoute path="/run-script" loginState={loggedIn} component={RunScriptPage}/>
                <PrivateRoute path="/script-logs" loginState={loggedIn} component={ScriptLogPage}/>
                <PrivateRoute path="/script-viewer" loginState={loggedIn} component={ScriptViewPage}/>
                <PrivateRoute path="/computerViewer" loginState={loggedIn} component={ComputerViewer}/>
                <PrivateRoute path="/error-doc" loginState={loggedIn} component={ErrorDoc}/>
              </Switch>
            </div>
          </Route>
            
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
