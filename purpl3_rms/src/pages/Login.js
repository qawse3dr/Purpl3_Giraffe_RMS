import React from 'react'
import './Login.css'
import logo from '../res/logo.png'
import axios from 'axios'

class Login extends React.Component {

    constructor(props){
        super(props);
    }

    render() {
        return (
        <div className="login-page">
            <div className="login-block">
                <img className="logo-img" src={logo}/>
                <p id="invalidCreds" style={{color: "red"}}></p>
                <label>Username</label>
                <input id = "username" type="text"/><br/>
                <label>Password</label>
                <input id = "password" type="password"/><br/><br/>
                <button className="btn" onClick={this.handleLogin}>Login</button>
            </div>
        </div>
        );
    }

    handleLogin = () => {
        let username = document.getElementById("username").value;
        let password = document.getElementById("password").value;

        axios.post("/login", {
            body: {
                op: "LOGIN",
                data: {
                    Username: username,
                    Password: password
                }
            }
            }).then((res) => {
              //alert(JSON.stringify(res.data))
              //Update login status
              if (res.data.Error.code == 0){
                  this.props.sendLoginStatus(true);
                  this.props.history.push("/run-script")
              } 
              else{//else -> invalid credentials, inform user
                document.getElementById("invalidCreds").innerHTML="Invalid username or password"
              }
            }).catch((res) =>{
              alert("Post Failed")
            })
    }

}

export default Login
