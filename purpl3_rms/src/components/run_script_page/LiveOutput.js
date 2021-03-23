import React from "react"
import axios from "axios";
import Button from '../Button'

class LiveOutput extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            script: props.test,
            computer: -1
        }

        this.handleUpdateScript = this.handleUpdateScript.bind(this);
    }

    handleUpdateScript() {
        this.setState(state => ({
            script: state.script + 1
        }));
    }

    render() {
    	return 	(
            <div>
				<button onClick={this.handleUpdateScript}>Test in Component</button>
				<h1>Output</h1>
				<h2>Running {this.state.script}, on {this.state.computer}</h2>
	        	<textarea readonly rows="4" cols="50">
	        		Run a program to view output!
	        	</textarea>
	        </div>
        );
    }
}

//Currently just the example from run scripts
function getOutput(){
  axios.post("/api", {
    body: {
      op:"GET_FILE",
      data:{
        ScriptID: 0,
        ComputerID: 0
      }
    }
    }).then((res) => {
      alert(JSON.stringify(res.data))
    }).catch((res) =>{
      alert("Post Failed")
    })
}

export default LiveOutput