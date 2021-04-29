
import axios from "axios";
import SelectTable from '../table/SelectTable.js';
import LiveOutput from "./LiveOutput.js";
import React, {useState , useEffect} from "react";
import { Button, Col, Container, Row} from 'react-bootstrap';
import './runScript.css';

const RunScriptPage = (props) => {
    const [showComputer, setComputer] = useState(-1);
    const [showScript, setScript] = useState(-1);
    const [showRunScript, setRunScript] = useState(-1);
    const [showConsoleType, setConsoleType] = useState("STDOUT");
    const [showFpSTDOUT, setFpSTDOUT] = useState(0);
    const [showFpSTDERR, setFpSTDERR] = useState(0);
    const [showOutputSTDOUT, setOutputSTDOUT] = useState("");
    const [showOutputSTDERR, setOutputSTDERR] = useState("");
    const [showScriptList, setScriptList] = useState([]);
    const [showCompList, setCompList] = useState([]);

    useEffect(() => {
        axios.post("/api", {
            body: {
                op: "MANAGE_SCRIPTS",
                data:{
                    funcOP: "GET_ALL",
                    data: {}
                }
            }
        }).then((res) => {
            setScriptList([...res.data.entries]);
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
            setCompList([...res.data.entries])
        }).catch((res) =>{
            console.log(res)
        })

    }, [setScriptList, setCompList])

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

                        <SelectTable value={showComputer} tableName="ComputerTable" input={showCompList} onChange={handleSelectComputer}/> {/*consider doing lambda function here and changing directly */}
                    </Col>
                    <Col>
                    
                        <SelectTable value={showScript} tableName="ScriptTable" input={showScriptList} onChange={handleSelectScript}/>
                    </Col>
                </Row>
            </Container>
        
            <div className="Run_Button">
                <Button className="outputButtons" size="lg" variant="success" type="button" onClick={handleRunScript}>Run Script</Button>
                <Button className="outputButtons" size="lg" variant="success" type="button" onClick={handleLiveOutput}>Refresh Output</Button>
            </div>
            
            <LiveOutput 
                stdout={showOutputSTDOUT}
                stderr={showOutputSTDERR}
                setConsoleType={handleConsoleType}
            />
        </div>
    );

    function handleSelectComputer(params){
        setComputer(params)
    }

    function handleSelectScript(params){
        setScript(params)
    }

    function handleConsoleType(consoleType){
        setConsoleType(consoleType);
        handleLiveOutput()
    }

    function handleRunScript() {
        //Backend call to run script
        axios.post("/api", {
            body: {
              op:"RUN_SCRIPT",
              data:{
                ScriptID: showScript.ID,
                ComputerID: showComputer.ID,
              }
            }
        }).then((res) => { //Sucess
            alert(JSON.stringify(res.data))   
            setRunScript(res.data.Id);

        }).catch((res) =>{ //Fail
            alert("Post Failed"); //Prob remove this final ver
            setRunScript(-1);
        })

        //Reset file position and output either way
        setFpSTDERR(0);
        setFpSTDOUT(0);
        setOutputSTDERR("");
        setOutputSTDOUT("");
    }

    //Call to backend to retrieve script output.
    function handleLiveOutput() {
        //Only run if the is a script actually running.
        if (showRunScript !== -1) {
            //Local variable of the current fileposition to reduce code
            let filePos;
            if (showConsoleType === "STDOUT") {
                filePos = showFpSTDOUT;
            } 
            else {
                filePos = showFpSTDERR;
            }

            //Backend Call for getting live output
            axios.post("/api", {
                body: {
                    op:"MANAGE_SCRIPT_LOGS",
                    data:{
                        funcOP:"GET_FILE",
                        data:{
                            Id: showRunScript, //return value of soory's handleRunScript()
                            Filetype: showConsoleType, //default of STDOUT
                            FP: filePos //default of 0
                        }
                    }
                }
            }).then((res) => { //Success
                //Update output textarea and FP depending on which consoleType
                if (showConsoleType === "STDOUT") { //STDOUT
                    setOutputSTDOUT(setOutputSTDOUT + res.data.entry)
                    setFpSTDOUT(res.data.FP)
                } 
                else { //STDERR
                    setOutputSTDERR(setOutputSTDERR + res.data.entry)
                    setFpSTDERR(res.data.FP)
                }

            }).catch((res) =>{ //Fail                
                //Reset file position and output
                setFpSTDERR(0);
                setFpSTDOUT(0);
                setOutputSTDERR("");
                setOutputSTDOUT("");

                alert("Post Failed.");
            })
        } 
        else {
            //Reset file position eitherway
            setFpSTDERR(0);
            setFpSTDOUT(0);
            setOutputSTDERR("");
            setOutputSTDOUT("");
        }
    }

}

export default RunScriptPage
