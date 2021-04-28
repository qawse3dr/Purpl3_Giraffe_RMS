import React from 'react'
import './Login.css'
import logo from '../res/logo.png'
import {Button, Form} from "react-bootstrap"
import axios from 'axios'

class Login extends React.Component {

    constructor(props){
        super(props);
        this.handleLogin = this.handleLogin.bind(this);

        
    }

    handleLogin(event) {
        event.preventDefault();
        event.stopPropagation();
        const form = event.currentTarget;
        let username = form.Username.value;
        let password = form.Password.value;

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
              console.log(res.data.Error.code)
              if (res.data.Error.code === 0){
                  this.props.sendLoginStatus(true);
                  this.props.history.push("/run-script")
              } 
              else{//else -> invalid credentials, inform user
                alert("Fail")
              }
            }).catch((res) =>{
              alert("Post Failed")
            })
    }

    render() {
        return (
        <div className="login-page">
            <Form noValidate className="login" onSubmit={this.handleLogin}>
                <img className="logo-img" src={logo} alt= "logo"/>
                <Form.Group controlId="Username">
                    <Form.Label>Username</Form.Label>
                    <Form.Control type="input" placeholder="Username"/>
                </Form.Group>
                <Form.Group controlId="Password">
                    <Form.Label>Password</Form.Label>
                    <Form.Control type="password" placeholder="Password"/>
                </Form.Group>
                
                <Button className="LoginBtn" variant="primary" type="submit">
                    Login
                </Button>
            </Form>
        </div>
        );
    }


}

export default Login
