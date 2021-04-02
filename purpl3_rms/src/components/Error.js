import React from "react"
import axios from "axios";
import Button from './Button'

function error(props) {
	return 	<div class="modal">
            <div class="modal_content">
              <span class="close">&times;</span>
              <p>I'm A Pop Up!!!</p>
            </div>
          </div>
}

class Popup extends React.Component {  
    render() {  
        return (  
            <div className='popup'>  
                <div className='popup\_inner'>  
                    <h1>{this.props.text}</h1>  
                    <button onClick={this.props.closePopup}>close me</button>  
                </div>  
            </div>  
        );  
    }  
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


export default Error