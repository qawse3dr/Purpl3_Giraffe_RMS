import React from 'react'
import LoginForm from '../components/LoginForm'

class InputField extends React.Component {
    render() {
        return (
            <LoginForm history={this.props.history}/>
        );
    }
}

export default InputField
