import React from 'react'

class Button extends React.Component {

    render() {
        return (
            <button className="btn"
                    color={this.props.color}
                    onClick={this.props.onClick}
                    style={{backgroundColor: this.props.color}}>
                {this.props.text}
            </button>
        );
    }
}

export default Button
