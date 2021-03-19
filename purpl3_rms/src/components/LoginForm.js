import React from 'react'
import Button from './Button'
import InputField from './InputField'
import './LoginForm.css'
import logo from '../res/logo.png'
import { useHistory } from 'react-router'

class LoginForm extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            username: '',
            password: ''
        }
    }

    click = () => {
        this.props.history.push("/run-script")
    }

    render() {
        return (
        <div className="login-page">
            <div className="login-block">
                <img className="logo" src={logo}/>
                <label>Username</label>
                <InputField type="text"/><br/>
                <label>Password</label>
                <InputField type="password"/><br/>
                <Button color="green" text="Login" onClick={this.click}/>
            </div>
        </div>
        );
    }
}

export default LoginForm
