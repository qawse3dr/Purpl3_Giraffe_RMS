import React from "react"
import axios from "axios";
import Button from '../Button'

//=========================================================================================
// CURRENTLY NOT USED AS THIS FUNCTIONALITY IS DIRECTLY BAKED INTO run_script_page_soory.js
//=========================================================================================

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

//Get output of script. Requires the ID of current script from Run_script().
function getLiveOutput(){
  axios.post("/api", {
    body: {
      op:"GET_FILE",
      data:{
        Id: 0,
        Filetype: "ENUM"
      }
    }
    }).then((res) => {
      alert(JSON.stringify(res.data))
    }).catch((res) =>{
      alert("Post Failed")
    })
}

export default LiveOutput