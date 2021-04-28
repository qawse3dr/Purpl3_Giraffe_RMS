import './scriptLogCSS.css';
import axios from "axios";
import SelectTable from '../table/SelectTable.js';
import LiveOutput from "../run_script_page/LiveOutput.js";
import React, {useState, useEffect} from "react";
import { Table } from 'react-bootstrap';

const ScriptLogPage = (props) => {
    const [script_log_List,setScriptLog_list] = useState([])
    const [pickedLog,setPickedLog] = useState(0)
    const [script, setScript] = useState(null);
    const [showDeleteLog, setShowDeleteLog] = useState(false)

    const [currentSTDOUT, setCurrentSTDOUT] = useState("")
    const [currentSTDERR, setCurrentSTDERR] = useState("")
    const [consoleType, setCurrentConsoleType] = useState("STDOUT")

    useEffect(() => {

        if (pickedLog === 0) {
            // TODO add logs
        }
        else{
            
            axios.post("/api", {
                body: {
                    op: "MANAGE_SCRIPT_LOGS",
                    data:{
                    funcOP: "GET_FILE",
                    data: {
                        Id: script.ID,
                        Filetype: consoleType,
                        FP: 0            
                    }
                    }
                }
                }).then((res) => {
                    if(consoleType === "STDOUT"){
                        setCurrentSTDOUT(res.data.entry)
                    }else {
                        setCurrentSTDERR(res.data.entry)
                    }
                }).catch((res) =>{
                    console.log(res)
                })
            
            
        }
    },[consoleType,pickedLog,script]);


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
            let input_list = []
            for (let index = res3.data.entries.length-1; index >= 0; index--) {
                let logs = res3.data.entries[index];
                input_list.push(logs);
            }

            if (input_list.length === 0) {
                input_list = [{name:"There are no logs"}]
            }
            else{
                input_list.forEach(element => {
                    let logs = element
                    logs["name"] = `Script Log: ${logs.ID} / `
                    computers.forEach(computer => {
                        
                        if (computer.ID === logs.compID) {
                            logs["name"] += "Computer: " + computer.nickName
                        }
                    });
                    scripts.forEach(script => {
                        if (script.ID === logs.scriptID) {
                            logs["name"] +="  / Script: " + script.name
                        }
                    });
                });
            }
            setScriptLog_list(old_list => input_list)
        }));
    }, []);



    function handleConsoleType(consoleType){
        setCurrentConsoleType(consoleType)
    };


    function Select_script(params)
    {
        setPickedLog(1);
        console.log(params)
        setScript(params);
        
    };

    return(
        <div className="h-100">
            
            <div className="title text-center">
            <h1>Select Log</h1>
            </div>
            
            <div className="ScriptLogsSelect">
                
                <SelectTable  value={script} tableName="scriptLogTable" input={script_log_List} onChange={Select_script}/>
                
            </div>
            <div className="action-buttons">
                <button style={{color:"red"}} onClick={() => setShowDeleteLog(!showDeleteLog)}>Delete Log</button>
            </div>
                
            {/* Information table about the script */}
            <Table striped bordered hover responsive variant="dark" size="lg" className="mb-0" >
              <thead>
                <tr>
                  <th>
                    Name
                  </th>
                  <th>
                    Error Code
                  </th>
                  <th>
                    Return Value
                  </th>
                  <th>
                    Start Time
                  </th>
                  <th>
                    End Time
                  </th>
                  <th>
                    Run As Admin
                  </th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>
                    {script != null ? script.ID : "Select A Script Log"}
                  </td>
                  <td>
                    {script != null ? script.errorCode : ""}
                  </td>
                  <td>
                    {script != null ? script.returnVal : ""}
                  </td>
                  <td>
                    {script != null ? script.startTime : ""}
                  </td>
                  <td>
                    {script != null ? script.endTime : ""}
                  </td>
                  <td>
                    {script != null ? script.asAdmin : ""}
                  </td>
                </tr>
              </tbody>
            </Table>
                
            
                
            

            <LiveOutput className="LiveOutput-ScriptLogs"
                    stdout={currentSTDOUT}
                    stderr={currentSTDERR}
                    setConsoleType={handleConsoleType}
                />
            
        </div>
        
    );
}









export default ScriptLogPage