import React, {useEffect, useContext} from 'react'
import './Login.css'
import logo from '../../res/logo.png'
import {Button, Form} from "react-bootstrap"
import { loginRequest, loginCheckRequest } from '../../libpurpl3/purpl3API'
import {ErrorContext} from "../../context/errorContext";
import {ErrorModal} from "../modals/errorModal"
const Login = (props) => {

    const [error, setError] = useContext(ErrorContext);

    useEffect(() => {
        loginCheckRequest().then((res) => {
            props.sendLoginStatus(true);
            props.history.push("/run-script")
        }).catch(res => {});
    // eslint-disable-next-line
    }, [])
    return(
        <div className="login-page">
            <Form noValidate className="login" onSubmit={handleLogin}>
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

    function handleLogin(event) {
        event.preventDefault();
        event.stopPropagation();
        const form = event.currentTarget;
        let username = form.Username.value;
        let password = form.Password.value;

        console.log("handleLogin")
        loginRequest(username, password).then(res => {
            props.sendLoginStatus(true);
            props.history.push("/run-script")
        }).catch(setError);
    }

}

export default Login
