import React from "react"
import axios from "axios";
import Button from './Button'

function LiveOutput(props) {
	return 	<div>
				<Button color="green" text="Run Script"/>
				<h1>Output</h1>
				<h2>Running {props.script}, on {props.computer}</h2>
	        	<textarea readonly rows="4" cols="50">
	        		Run a program to view output!
	        	</textarea>
	        </div>
}

//Example of running a script
function runScript(){
  axios.post("/api", {
    body: {
      op:"RUN_SCRIPT",
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