import React from 'react'

class InputField extends React.Component {
    render() {
        return (
            <div className="inputField">
                <input 
                    className="input"
                    type={this.props.type}
                ></input>
                        
            </div>
        );
    }
}

export default InputField
