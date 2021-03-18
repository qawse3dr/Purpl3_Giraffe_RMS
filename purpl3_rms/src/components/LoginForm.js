import React from 'react'
import Button from './Button'
import InputField from './InputField'
import './LoginForm.css'
import logo from '../res/logo.png'

class LoginForm extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            username: '',
            password: ''
        }
    }

    render() {
        return (
            <div className="login-block">
                <img className="logo" src={logo}/>
                <label>Username</label>
                <InputField type="text"/><br/>
                <label>Password</label>
                <InputField type="password"/><br/>
                <Button color="green" text="Login" onClick=""/>
            </div>
        );
    }
}

export default LoginForm
