import './scriptLog.css';
import SelectTable from '../selectTable/selectTable.js';
import LiveOutput from "../runScript/LiveOutput.js";
import React, {useState, useEffect} from "react";
import { Table, Button } from 'react-bootstrap';
import { getScriptLogs, getAllComputers, getAllScripts, getAllScriptLogs, deleteScriptLogs} from "../../purpl3API/purpl3API";

const ScriptLogPage = (props) => {
    const [script_log_List,setScriptLog_list] = useState([])
    const [pickedLog,setPickedLog] = useState(0)
    const [script, setScript] = useState(null);
    const [showDeleteLog, setShowDeleteLog] = useState(false)

    const [currentSTDOUT, setCurrentSTDOUT] = useState("")
    const [currentSTDERR, setCurrentSTDERR] = useState("")
    const [consoleType, setCurrentConsoleType] = useState("STDOUT")

    const [refresh , setRefresh] = useState(true)
    useEffect(() => {

        if (pickedLog === 0 || !script) {
            console.log("script is null")
        }
        else{
            getScriptLogs(script.ID, 0, consoleType).then(res => {
              if(consoleType === "STDOUT"){
                setCurrentSTDOUT(res.data.entry)
              }else {
                setCurrentSTDERR(res.data.entry)
              }
            }).catch(res => {

            })           
            
        }
    },[consoleType,pickedLog,script]);

    useEffect(() => {
      //only refresh if refresh is true
      async function retrieveScriptLogs(){
        let scriptLogs = (await getAllScriptLogs()).data.entries;
        let scripts = (await getAllScripts()).data.entries;
        let computers = (await getAllComputers()).data.entries;

        let input_list = []
        for (let index = scriptLogs.length-1; index >= 0; index--) {
          let logs = scriptLogs[index];
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
        setScriptLog_list(input_list)
      }
      retrieveScriptLogs();
    }, [refresh]);

    function handleConsoleType(consoleType){
        setCurrentConsoleType(consoleType)
    };

    function Select_script(params)
    {
        setPickedLog(1);
        console.log(params)
        setScript(params);
        
    };
    
    function deleteLog(){
      if(script !== null){
        deleteScriptLogs(script.ID).then(res => {
          setRefresh(!refresh);
        }).catch(res => {
          setRefresh(!refresh)
        })

      }
    }
    return(
        <div className="h-100">
            
            <div className="title text-center">
            <h1>Select Log</h1>
            </div>
            
            <div className="ScriptLogsSelect">
                
                <SelectTable  value={script} tableName="scriptLogTable" input={script_log_List} onChange={Select_script}/>
                
            </div>
            <div className="action-buttons">
              <Button onClick={() => {deleteLog();setShowDeleteLog(true)}}  className="font-weight-bolder" variant="danger">Delete</Button>
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