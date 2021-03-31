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

    	axios.post("/api", {
            body: {
                op:"MANAGE_COMPUTERS",
                funcOP: "GET_ALL",
                data:{
              //   	SearchAttribute: See: DB
		            // Value1: string 
		            // Value2: string | NULL
		            // SortAttribute: See: DB
		            // SortType: ENUM
                }
            }
        }).then((res) => {
            //alert("Success");
        }).catch((res) =>{
            //alert("Post Failed")
        })


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
	                op:"MANAGE_COMPUTERS",
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
	        }).then((res) => {
	            alert("Success! Computer added.");
	            message.innerHTML = "Success! Computer added.";

	            //Clearing fields after successfully adding
	            document.getElementById("name").value = "";
		        description = "";
		        username = "";
		        password = "";
		        ip = "";

	        }).catch((res) =>{
	            alert("Post Failed");
	            message.innerHTML = "Error: Failed to add computer.";
	        })
        } else {
        	message.innerHTML = "Please fill in all the blanks!";
        }
        
    }

    render() {
        return (
            <div>
            	<h1>Computer Manager</h1>

            	<h2>Adding Computer</h2>
                <label>Computer Name</label>
                <input id = "name" type="text"/><br/>
                <label>Computer Description</label>
                <input id = "description" type="text"/><br/>
                <label>Computer Username</label>
                <input id = "username" type="text"/><br/>
                <label>Computer Password</label>
                <input id = "password" type="password"/><br/>
                <label>Computer IP</label>
                <input id = "ip" type="text"/><br/>

                <p id="message"></p>
                <button className="btn" onClick={this.handleAddComputer}>Add Computer</button>
            </div>
        );
    }
}

export default Computer;
