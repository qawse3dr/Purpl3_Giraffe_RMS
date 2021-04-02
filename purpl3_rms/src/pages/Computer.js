import './Computer.css';
import React from 'react';
import axios from 'axios'

class Computer extends React.Component {
    constructor(props){
        super(props);
        this.state = {
        }

        this.handleAddComputer = this.handleAddComputer.bind(this);
    }

    componentDidMount() {
    	//alert("Computer mounted");

    	// axios.post("/api", {
     //        body: {
     //            op:"MANAGE_COMPUTERS",
     //            funcOP: "GET_ALL",
     //            data:{}
     //            }
     //        }
     //    }).then((res) => {
     //        alert("Success");
     //        for (let x in res.data.enties) {
     //        	alert(x)
     //        }
     //    }).catch((res) =>{
     //        alert("Post Failed")
     //    })


		//If Value2 == NULL, search for equals or contains value1
		//If Value2 !=NULL, search for between value1 and value2 
		//SortType will either be ascending or descending based on enum

  	}

    handleAddComputer() {
        let name = document.getElementById("name");
        let description = document.getElementById("description");
        let username = document.getElementById("username");
        let password = document.getElementById("password");
        let ip = document.getElementById("ip");

        let message = document.getElementById("message");

        if (name.value != "" && description.value != "" && username.value != "" && password.value != "" && ip.value != "") {
        	axios.post("/api", {
            	body: {
	                op:"MANAGE_COMPUTER",
                    data:{
                        funcOP: "ADD",
                        data:{
                            Name: name.value,
                            Desc: description.value,
                            Username: username.value,
                            Password:  password.value,
                            IP: ip.value,
                            isAdmin: false
                        }
                    }
	            }
	        }).then((res) => {
	        	
	        	//Post request might go through, though an error could still occur such as incorrect fields.
	        	if (res.data.Error.code == 0) {
					alert("Success! Computer added.");
		            message.innerHTML = "Success! Computer added.";

		            //Clearing fields after successfully adding
		            name.value = "";
			        description.value = "";
			        username.value = "";
			        password.value = "";
			        ip.value = "";
	        	} else {
	        		message.innerHTML = "Error: Failed to add computer.";
	        		alert("Post Success, error " + res.data.Error.code + ": " + res.data.Error.reason);
	        	}

	        }).catch((res) =>{

	            message.innerHTML = "Error: Failed to add computer.";
	            alert("Post Failed.");

	        })
        } else {
        	message.innerHTML = "Please fill in all the blanks!";
        }
        
    }

    render() {
        return (
            <div>
            	<h1>Computer Manager</h1>

            	<div class="addComputer">
	            	<h2>Adding Computer</h2>
	            	<p>
		                <label>Computer Name</label><br/>
		                <input class="textArea" id="name" type="text"/>
		            </p>
		            <p>
		                <label>Computer Description</label><br/>
		                <input class="textArea" id="description" type="text"/>
	                </p>
	                <p>
		                <label>Computer Username</label><br/>
		                <input class="textArea" id="username" type="text"/>
	                </p>
	                <p>
		                <label>Computer Password</label><br/>
		                <input class="textArea" id="password" type="password"/>
	                </p>
	                <p>
		                <label>Computer IP</label><br/>
		                <input class="textArea" id="ip" type="text"/>
	                </p>
	            </div>

                <p id="message"></p>
                <button className="btn" onClick={this.handleAddComputer}>Add Computer</button>
            </div>
        );
    }
}

export default Computer;
