import './run_script_page.css';
import axios from "axios";
import Table from '../table/table_soory.js';
import React from "react";

class RunScriptPage extends React.Component {
    constructor() {
        super();
        this.state = {
            runningScript: -1,
            consoleType: "STDOUT",
            filePositionSTDOUT: 0,
            filePositionSTDERR: 0,
            currentOutputSTDOUT: "",
            currentOutputSTDERR: ""
        }

        this.handleRunScript = this.handleRunScript.bind(this);
        this.handleLiveOutput = this.handleLiveOutput.bind(this);
        this.handleDisplaySTDOUT = this.handleDisplaySTDOUT.bind(this);
        this.handleDisplaySTDERR = this.handleDisplaySTDERR.bind(this);
    }

    handleRunScript() {
        let in_computer = document.getElementById("Select_Computer_text");
        let in_script = document.getElementById("Select_Script_text");

        //Backend call to run script
        axios.post("/api", {
            body: {
              op:"RUN_SCRIPT",
              data:{
                ScriptID: in_script.value,
                ComputerID: in_computer.value
              }
            }
        }).then((res) => { //Sucess
            alert(JSON.stringify(res.data))
            //let btn = document.getElementById("run_page_runbtn");
            //btn.value = res.data;
            //console.log(btn.value.Id);
        
            //Updating the currently running script to be the return of this function call
            this.setState(state => ({
                runningScript: res.data.Id,
            }));

        }).catch((res) =>{ //Fail
            alert("Post Failed"); //Prob remove this final ver

            //Update the currently running script to be -1 or nothing
            this.setState(state => ({
                runningScript: -1,
            }));
            document.getElementById("Live_Output").value = "Running the script failed. Try again";
        })

        //Reset file position and output eitherway
        this.setState(state => ({
            filePositionSTDOUT: 0,
            filePositionSTDERR: 0,
            currentOutputSTDOUT: "",
            currentOutputSTDERR: "",
        }));
    }

    //Call to backend to retrieve script output.
    handleLiveOutput() {
        //Only run if the is a script actually running.
        if (this.state.runningScript != -1) {
            //Local variable of the current fileposition to reduce code
            let filePos;
            if (this.state.consoleType == "STDOUT") {
                filePos = this.state.filePositionSTDOUT;
            } else {
                filePos = this.state.filePositionSTDERR;
            }

            //Backend Call for getting live output
            axios.post("/api", {
                body: {
                    op:"MANAGE_SCRIPT_LOGS",
                    data:{
                        funcOP:"GET_FILE",
                        data:{
                            Id: this.state.runningScript, //return value of soory's handleRunScript()
                            Filetype: this.state.consoleType, //default of STDOUT
                            FP: filePos //default of 0
                        }
                    }
                }
            }).then((res) => { //Success
                //alert(JSON.stringify(res.data))

                //Update output textarea and FP depending on which consoleType
                if (this.state.consoleType === "STDOUT") { //STDOUT
                    this.setState(state => ({
                        currentOutputSTDOUT: state.currentOutputSTDOUT + res.data.entry,
                        filePositionSTDOUT: res.data.FP
                    }));
                    document.getElementById("Live_Output").value = this.state.currentOutputSTDOUT;

                } else { //STDERR
                    this.setState(state => ({
                        currentOutputSTDERR: state.currentOutputSTDERR + res.data.entry,
                        filePositionSTDERR: res.data.FP
                    }));
                    document.getElementById("Live_Output").value = this.state.currentOutputSTDERR;
                }

            }).catch((res) =>{ //Fail
                document.getElementById("Live_Output").value = "Something went wrong with getting the live output :C. Please try again.";
                
                //Reset file position and output
                this.setState(state => ({
                    filePositionSTDOUT: 0,
                    filePositionSTDERR: 0,
                    currentOutputSTDOUT: "",
                    currentOutputSTDERR: ""
                }));

                alert("Post Failed.");
            })
        } else {
            document.getElementById("Live_Output").value = "Run a script first before checking the live output!"

            //Reset file position eitherway
            this.setState(state => ({
                filePositionSTDOUT: 0,
                filePositionSTDERR: 0,
                currentOutputSTDOUT: "",
                currentOutputSTDERR: ""
            }));
        }
    }

    handleDisplaySTDOUT() {
        this.setState(state => ({
            consoleType: "STDOUT"
        }));
        document.getElementById("displayLabel").innerHTML = "Displaying: STDOUT";
        document.getElementById("Live_Output").value = this.state.currentOutputSTDOUT;
    }

    handleDisplaySTDERR() {
        this.setState(state => ({
            consoleType: "STDERR",
        }));
        document.getElementById("displayLabel").innerHTML = "Displaying: STDERR";
        document.getElementById("Live_Output").value = this.state.currentOutputSTDERR;
    }

    render() {
        return (
            <div>
                <div className="body">
                    <div className="column">
                        <h1>Select Computer</h1>
                        <div className="scroll">
                            <Table input={[ {name:'Soory\'s computer\tIp:123.1234.7777',script:Select_computer_func},
                                            {name:'Larry\'s computer\tIp:123.1234.7777',script:Select_computer_func},
                                            {name:'Julian\'s computer\tIp:123.1234.7777',script:Select_computer_func},
                                            {name:'Rachael\'s computer\tIp:123.1234.7777',script:Select_computer_func},
                                            {name:'Daniela\'s computer\tIp:123.1234.7777',script:Select_computer_func},
                                            {name:'James\'s computer\tIp:123.1234.7777',script:Select_computer_func}]}/>
                        </div>
                    </div>

                    <div className="column">
                        <h1>Select Script</h1>
                        <div className="scroll">
                            <Table input={[ {name:'Shutdown computer',script:Select_script_func},
                                            {name:'Install Libre Office',script:Select_script_func},
                                            {name:'Send meeting email',script:Select_script_func},
                                            {name:'Order apple juice',script:Select_script_func},
                                            {name:'Toggle smart lights',script:Select_script_func},
                                            {name:'Cancel apple juice',script:Select_script_func}]}/>
                        </div>
                    </div>

                    <p id="Select_Computer_text"></p>
                    <p id="Select_Script_text"></p>
                </div>

                <footer>
                    <div className="Run_Button">
                        <button class="button" type="button" onClick={this.handleRunScript}>Run Script</button>
                        <button class="button" type="button" onClick={this.handleLiveOutput}>Refresh Output</button>
                    </div>
                    
                    <p id="displayLabel">Displaying: STDOUT</p>
                    <button class="tab" onClick={this.handleDisplaySTDOUT}>stdout</button>
                    <button class="tab" onClick={this.handleDisplaySTDERR}>stderr</button>  

                    <textarea id="Live_Output" readonly rows="10" cols="200">
                        Run a program to view it's output!
                    </textarea>
                </footer>
            </div>
        );
    }
}

function Select_computer_func(parms){
    let text = document.getElementById("Select_Computer_text");
    text.textContent = "Selected Computer : " + parms.name;
    text.value = parms.name;
}

function Select_script_func(parms){
    let text = document.getElementById("Select_Script_text");
    text.textContent = "Selected Script : " + parms.name;
    text.value = parms.name;
}
  
export default RunScriptPage
