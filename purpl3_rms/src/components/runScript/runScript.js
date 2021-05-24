import SelectTable from '../selectTable/selectTable.js';
import LiveOutput from "./LiveOutput.js";
import React, {useState , useEffect, useContext} from "react";
import { Button, Col, Container, Row} from 'react-bootstrap';
import {getAllScripts, getAllComputers, runScript, getScriptLogs} from "../../libpurpl3/purpl3API"
import './runScript.css';
import {ErrorContext} from "../../context/errorContext";

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
    const [error, setError] = useContext(ErrorContext);

    useEffect(() => {
        getAllScripts().then(res => {
            setScriptList(res.data.entries);
        }).catch(setError);
        
        getAllComputers().then(res => {
            for(let entry of res.data.entries){
                entry.name = entry.nickName;
            }
            setCompList(res.data.entries)
        }).catch(setError)
            

    }, [setScriptList, setCompList])

    
    useEffect(() => {
        handleLiveOutput();
    // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [showConsoleType, showRunScript]);
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
                <Row className="select-boxes">
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

    // FIXME - null issue
    async function handleConsoleType(consoleType){
        await setConsoleType(consoleType);
        handleLiveOutput()
    }

    function handleRunScript() {
        //Backend call to run script
        if(showScript && showComputer){
            runScript(showScript.ID, showComputer.ID).then(res => {
                setRunScript(res.data.Id);
                alert(res.data.Error)
            }).catch(res =>{
                setRunScript(-1);
                setError(res);
            })

        }

        //Reset file position and output either way
        setFpSTDERR(0);
        setFpSTDOUT(0);
        setOutputSTDERR("");
        setOutputSTDOUT("");
    }

    //Call to backend to retrieve script output.
    function handleLiveOutput(){
        
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
            getScriptLogs(showRunScript,filePos,showConsoleType).then(res => {
                //Update output textarea and FP depending on which consoleType
                if (showConsoleType === "STDOUT") { //STDOUT
                    setOutputSTDOUT(showOutputSTDOUT + res.data.entry)
                    setFpSTDOUT(res.data.FP)
                } 
                else { //STDERR
                    setOutputSTDERR(showOutputSTDERR + res.data.entry)
                    setFpSTDERR(res.data.FP)
                }
            }).catch((res) =>{ //Fail                
                //Reset file position and output
                setFpSTDERR(0);
                setFpSTDOUT(0);
                setOutputSTDERR("");
                setOutputSTDOUT("");
                setError(res);
            });
            
        } 
        else {
            //Reset file position either way
            setFpSTDERR(0);
            setFpSTDOUT(0);
            setOutputSTDERR("");
            setOutputSTDOUT("");
        }
    }

}

export default RunScriptPage
