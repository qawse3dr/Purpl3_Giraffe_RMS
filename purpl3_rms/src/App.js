import logo from './res/logo.png';
import logoutBtn from "./res/logout.png"
import './App.css';
import React, {useState} from 'react';
import {
  Route,
  Switch,
  HashRouter
} from "react-router-dom";
import {Navbar, Nav, Modal, Button } from 'react-bootstrap'
import Login from './components/login/Login';
import RunScriptPage from './components/runScript/runScript';
//import Schedule from 
import ScriptLogPage from './components/scriptLog/scriptLog';
// import ScriptsViewer from './pages/ScriptsViewer'
import ScriptViewPage from './components/scriptView/scriptView';

import ErrorDoc from './components/errorDoc/errorDoc'
import ComputerPage from './components/computers/computers'
import PrivateRoute from './components/PrivateRoute'
import {LinkContainer} from "react-router-bootstrap"
import { logoutRequest } from './libpurpl3/purpl3API';
import {ErrorModal} from "./components/modals/errorModal"
import {ErrorContext} from "./context/errorContext";


function App() {

  const [loggedIn, setLogin] = useState(false);
  const [error, setError] = useState(null);

  return (
    <div className="App">
      <ErrorContext.Provider value={[error, setError]}>

      
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
                  <PrivateRoute path="/computerViewer" loginState={loggedIn} component={ComputerPage}/>
                  <PrivateRoute path="/error-doc" loginState={loggedIn} component={ErrorDoc}/>
                </Switch>
              </div>
            </Route>
              
            </Switch>
        </HashRouter>

        <ErrorModal
          show={error}
          onHide={() => {setError(null)}}
          error={error}
        />
      </ErrorContext.Provider>

      
      
      
    </div>
  );

  function getLoginStatus(loginState){
    setLogin(loginState)
  }

  function handleLogout(){
    logoutRequest().then(res =>{
      setLogin(false);
    });
    
  }
}

export default App;
