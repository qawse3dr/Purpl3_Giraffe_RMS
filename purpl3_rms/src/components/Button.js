import React from 'react'

class Button extends React.Component {

    onClick = () => {
        alert('Click!')
    }

    render() {
        return (
            <button className="btn"
                    color={this.props.color}
                    onClick={this.onClick}
                    style={{backgroundColor: this.props.color}}>
                {this.props.text}
            </button>
        );
    }
}

export default Button
