import './scriptLogCSS.css';
import axios from "axios";
import Table from '../table/table_soory.js';
import React, {useState ,useRef, Component, useEffect} from "react";

const ScriptLogPage = (props) => {
    const [script_log_List,setScriptLog_list] = useState([])
    const [pickedLog,setPickedLog] = useState(0)

    useEffect(() => {
        axios.all([
            axios.post("/api", {
                body: {
                  op: "MANAGE_SCRIPTS",
                  data:{
                    funcOP: "GET_ALL",
                    data: {}
                  }
                }
                }),
            axios.post("/api", {
                body: {
                    op: "MANAGE_COMPUTER",
                    data:{
                    funcOP: "GET_ALL",
                    data: {}
                    }
                }
                }),
            axios.post("/api", {
                body: {
                    op: "MANAGE_SCRIPT_LOGS",
                    data:{
                    funcOP: "GET_ALL",
                    data: {}
                    }
                }
                })
        ]).then(axios.spread((res1, res2, res3) => {
            let scripts = res1.data.entries
            let computers = res2.data.entries
            let input_list = res3.data.entries

            if (input_list.length == 0) {
                input_list = [{name:"There are no logs"}]
            }
            else{
                input_list.forEach(element => {
                    let logs = element
                    logs["name"] = ""
                    computers.forEach(computer => {
                        
                        if (computer.ID == logs.compID) {
                            logs["name"] += "Computer: " + computer.nickName
                        }
                    });
                    scripts.forEach(script => {
                        if (script.ID == logs.scriptID) {
                            logs["name"] +="  / Script: " + script.name
                        }
                    });
                    logs["name"] += "  / StartTime: " + logs.startTime +" / EndTime: "+ logs.endTime
                });
            }
            setScriptLog_list(old_list => input_list)
        }));
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
                axios.post("/api", {
                    body: {
                      op: "MANAGE_SCRIPT_LOGS",
                      data:{
                        funcOP: "GET_FILE",
                        data: {
                            Id: text.log.ID,
                            Filetype: "STDERR",
                            FP: 0           
                        }
                      }
                    }
                    }).then((res) => {
                        text.value = res.data.entry
                    }).catch((res) =>{
                      console.log(res)
                    })
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
                axios.post("/api", {
                    body: {
                      op: "MANAGE_SCRIPT_LOGS",
                      data:{
                        funcOP: "GET_FILE",
                        data: {
                            Id: text.log.ID,
                            Filetype: "STDOUT",
                            FP: 0            
                        }
                      }
                    }
                    }).then((res) => {
                        text.value = res.data.entry
                    }).catch((res) =>{
                      console.log(res)
                    })
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
            axios.post("/api", {
                body: {
                  op: "MANAGE_SCRIPT_LOGS",
                  data:{
                    funcOP: "GET_FILE",
                    data: {
                        Id: prams.current_object.ID,
                        Filetype: "STDOUT",
                        FP: 0      
                    }
                  }
                }
                }).then((res) => {
                    text.value = res.data.entry
                }).catch((res) =>{
                  console.log(res)
                })
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