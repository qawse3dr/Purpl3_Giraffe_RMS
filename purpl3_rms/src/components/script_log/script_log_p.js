import './scriptLogCSS.css';
import axios from "axios";
import Table from '../table/table_soory.js';
import React, {useState ,useRef, Component, useEffect} from "react";

const ScriptLogPage = (props) => {
    const [script_log_List,setScriptLog_list] = useState([])
    const [script_list,setScript_list] = useState([])
    const [computer_list,setComputer_list] = useState([])
    const [pickedLog,setPickedLog] = useState(0)

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
                setScript_list(old_list => [...res.data.entries])
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
                setComputer_list(old_list => [...res.data.entries])
            }).catch((res) =>{
                console.log(res)
            })

        axios.post("/api", {
            body: {
              op: "MANAGE_SCRIPT_LOGS",
              data:{
                funcOP: "GET_ALL",
                data: {}
              }
            }
            }).then((res) => {
                let input_list = [...res.data.entries]
                //let input_list = [{compID:1,scriptID:1,startTime:"now",endTime:"later",stdoutFile:"yo this is out",stderrFile:"yo this is error"}]
                let script_name = "nothing"
                let computer_name = "nothing"
                if (input_list.length == 0) {
                    input_list = [{name:"There are no logs"}]
                }
                else{
                    
                    input_list.forEach(element => {
                        let logs = element
                        script_list.forEach(scripts => {
                            if (scripts.ID == logs.scriptID) {
                                script_name = scripts.name
                            }
                        });
                        computer_list.forEach(computers => {
                            if (computers.ID == logs.compID) {
                                computer_name = computers.name
                            }
                        });
                        logs["name"] ="Computer: "+ computer_name + "  / Script: " + script_name + "  / Time:" + logs.startTime +" "+ logs.endTime
                    });
                }
                setScriptLog_list(old_list => input_list)
            }).catch((res) =>{
              alert("Post Failed")
            })
    }, []);

    function handleDisplaySTDERR(prams)
    {
        let text = document.getElementById("Log_Output");
        if (pickedLog == 0) {
            text.value = "Click on a Script to get the logs";
        }
        else{
            if (text.name == "There are no logs") {
                text.value = "There are no logs";
            }
            else{
                text.value = "STDERR : " + text.log.stderrFile;
            }
        }
    }

    function handleDisplaySTDOUT(prams)
    {
        let text = document.getElementById("Log_Output");
        if (pickedLog == 0) {
            text.value = "Click on a Script to get the logs";
        }
        else{
            if (text.name == "There are no logs") {
                text.value = "There are no logs";
            }
            else{
                text.value = "STDOUT: " + text.log.stdoutFile;
            }
        }
    }

    function Select_script(prams)
    {
        let text = document.getElementById("Log_Output");
        text.name = prams.current_object.name;
        setPickedLog(1);
        if (prams.name == "There are no logs") {
            text.value = "There are no logs";
        }
        else{
            text.value = "STDOUT: " + prams.current_object.stdoutFile;
            text.log = prams.current_object;
        }
        
    }

    return(
        <div>
            <div className="body">
                
                <div className="column4">
                    <h2>Select Log</h2>
                    <br></br>
                    <br></br>
                    <div className="scroll">
                        <Table input={script_log_List} onClickFunc={Select_script}/>
                    </div>
                </div>

                <div className="column">
                    <h2>Output</h2>
                    <div>
                        <button className="tab" onClick={handleDisplaySTDOUT}>stdout</button>
                        <button className="tab" onClick={handleDisplaySTDERR}>stderr</button>  
                    </div>
                    <textarea name="There are no logs" id="Log_Output" readOnly={true} rows="10" cols="110" defaultValue="Click on a Script to get the logs"/>
                </div>
                
            </div>
        </div>
        
    );
}









export default ScriptLogPage