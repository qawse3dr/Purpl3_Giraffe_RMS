
import axios from "axios";
import SelectTable from '../table/SelectTable.js';
import LiveOutput from "./LiveOutput.js";
import React from "react";
import { Button, Col, Container, Row} from 'react-bootstrap';
import './run_script_page.css';
class RunScriptPage extends React.Component {
    constructor() {
        super();
        this.state = {
            selectedComputer: -1,
            selectedScript: -1,
            runningScript: -1,
            consoleType: "STDOUT",
            filePositionSTDOUT: 0,
            filePositionSTDERR: 0,
            currentOutputSTDOUT: "",
            currentOutputSTDERR: "",
            script_list: [],
            computer_list: []
        }

        this.handleRunScript = this.handleRunScript.bind(this);
        this.handleLiveOutput = this.handleLiveOutput.bind(this);
        this.handleSelectComputer = this.handleSelectComputer.bind(this);
        this.handleSelectScript = this.handleSelectScript.bind(this);
        this.handleConsoleType = this.handleConsoleType.bind(this);
    }

    componentDidMount() {
        axios.post("/api", {
          body: {
            op: "MANAGE_SCRIPTS",
            data:{
              funcOP: "GET_ALL",
              data: {}
            }
          }
          }).then((res) => {
            this.setState(state => ({
              script_list: [...res.data.entries]
            }));
          }).catch((res) =>{
            alert("Post Failed")
          })
        
        axios.post("/api", {
            body: {
              op: "MANAGE_COMPUTER",
              data:{
                funcOP: "GET_ALL",
                data: {}
              }
            }
            }).then((res) => {
                for(let entry of res.data.entries){
                    entry.name = entry.nickName;
                }
                this.setState(state => ({
                    computer_list: [...res.data.entries]
                }));
            }).catch((res) =>{
              console.log(res)
            })
      }

    handleRunScript() {
        //Backend call to run script
        axios.post("/api", {
            body: {
              op:"RUN_SCRIPT",
              data:{
                ScriptID: this.state.selectedScript.ID,
                ComputerID: this.state.selectedComputer.ID,
              }
            }
        }).then((res) => { //Sucess
            alert(JSON.stringify(res.data))   
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
        })

        //Reset file position and output either way
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
        if (this.state.runningScript !== -1) {
            //Local variable of the current fileposition to reduce code
            let filePos;
            if (this.state.consoleType === "STDOUT") {
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
                    //document.getElementById("Live_Output").value = this.state.currentOutputSTDOUT;

                } else { //STDERR
                    this.setState(state => ({
                        currentOutputSTDERR: state.currentOutputSTDERR + res.data.entry,
                        filePositionSTDERR: res.data.FP
                    }));
                    //document.getElementById("Live_Output").value = this.state.currentOutputSTDERR;
                }

            }).catch((res) =>{ //Fail
                //document.getElementById("Live_Output").value = "Something went wrong with getting the live output :C. Please try again.";
                
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
            //document.getElementById("Live_Output").value = "Run a script first before checking the live output!"

            //Reset file position eitherway
            this.setState(state => ({
                filePositionSTDOUT: 0,
                filePositionSTDERR: 0,
                currentOutputSTDOUT: "",
                currentOutputSTDERR: ""
            }));
        }
    }

    
    handleSelectComputer(params){
        this.setState(state => ({selectedComputer: params}));
    }
    
    handleSelectScript(params){
        this.setState(state => ({selectedScript: params}));
    }

    handleConsoleType(consoleType){
        this.setState(state => ({consoleType: consoleType}), () =>{
            this.handleLiveOutput()
        })
    }
    render() {
        return (
            <div className="runScript">
                
                {/* Select computer and script*/}
                <Container className="selectContainer">
                    <Row className="text-center">
                        <Col>
                            <h3>Computer</h3>
                        </Col>
                        <Col>
                            <h3>Script</h3>    
                        </Col>
                    </Row>
                    <Row>
                        <Col>

                            <SelectTable value={this.state.selectedComputer} tableName="ComputerTable" input={this.state.computer_list} onChange={this.handleSelectComputer}/>
                        </Col>
                        <Col>
                        
                            <SelectTable value={this.state.selectedScript} tableName="ScriptTable" input={this.state.script_list} onChange={this.handleSelectScript}/>
                        </Col>
                    </Row>
                </Container>
            
                <div className="Run_Button">
                    <Button className="outputButtons" size="lg" variant="success" type="button" onClick={this.handleRunScript}>Run Script</Button>
                    <Button className="outputButtons" size="lg" variant="success" type="button" onClick={this.handleLiveOutput}>Refresh Output</Button>
                </div>
                
                <LiveOutput 
                    stdout={this.state.currentOutputSTDOUT}
                    stderr={this.state.currentOutputSTDERR}
                    setConsoleType={this.handleConsoleType}
                />

            </div>
        );
    }
}

  
export default RunScriptPage
