import axios from "axios";
import SelectTable from '../table/SelectTable';
import React, {useState , useEffect} from "react";
import {Table, Button, ButtonGroup} from "react-bootstrap";
import CreateScript from './CreateScript';
import DeleteScript from './DeleteScript';
import EditScript from './EditScript'

const ScriptViewpage = (props) => {
    const [numScripts, setNumScripts] = useState(0)
    const [list, setScript_list] = useState([])
    const [showAddScript, setShowAddScript] = useState(false);
    const [selectedScript, setSelectedScript] = useState(null)
    const [showDeleteScript, setShowDeleteScript] = useState(false);
    const [showEditScript, setShowEditScript] = useState(false);
    const [showScriptData, setShowScriptData] = useState("");
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
              setScript_list(res.data.entries)
              console.log(res.data.entries)
            }).catch((res) =>{
              alert("Post Failed")
            })
    }, [numScripts])

    return(
        <div className="scriptViewerContainer">
            <div className="title text-center">
              <h3>
                Script Viewer
              </h3>
            </div>
            <div className="scrollScriptLogs">
                <SelectTable value={selectedScript} tableName="scriptTable" input={list} onChange={Select_script}/>
            </div>
            
            
            <div className="action-buttons">
            <ButtonGroup className="font-weight-bold">
              <Button onClick={() => {setShowEditScript(true)}} className="font-weight-bolder" variant="primary">Edit</Button>
              <Button onClick={() => {setShowDeleteScript(true)}}  className="font-weight-bolder" variant="danger">Delete</Button>
              <Button onClick={() => {setShowAddScript(true)}} className="font-weight-bolder" variant="success">Create</Button>
            </ButtonGroup>
          </div>
            {showAddScript && <CreateScript addScript={Add} closeForm={closeAddScript}/>}
            {showEditScript && <EditScript scriptid={selectedScript.ID} editScript={Edit} closeForm={closeEditScript}/>}
            {showDeleteScript && <DeleteScript deleteScript={Delete} closeForm={closeDeleteScript}/>}

            {/* Information table about the script */}
            <Table striped bordered hover responsive variant="dark" size="lg" className="mb-0" >
              <thead>
                <tr>
                  <th>
                    Name
                  </th>
                  <th>
                    Description
                  </th>
                  <th>
                    File name
                  </th>
                  <th>
                    Size(B)
                  </th>
                  <th>
                    Date Created
                  </th>
                  <th>
                    Date Modified
                  </th>
                  <th>
                    Admin Script
                  </th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>
                    {selectedScript != null ? selectedScript.name : "Select A Script"}
                  </td>
                  <td>
                    {selectedScript != null ? selectedScript.desc : ""}
                  </td>
                  <td>
                    {selectedScript != null ? selectedScript.fileName : ""}
                  </td>
                  <td>
                    {selectedScript != null ? selectedScript.size : ""}
                  </td>
                  <td>
                    {selectedScript != null ? selectedScript.dtCreated : ""}
                  </td>
                  <td>
                    {selectedScript != null ? selectedScript.dtModified : ""}
                  </td>
                  <td>
                    {selectedScript != null ? selectedScript.isAdmin : ""}
                  </td>
                </tr>
              </tbody>
            </Table>

            <div className="scriptOutputContainer">
              <textarea readonly className="scriptOutput bg-secondary text-white"  value={showScriptData}></textarea>
            </div>
            

        </div>
    );

    function showScript(script){
      axios.post("/api", {
        body: {
            op:"MANAGE_SCRIPTS",
            data:{
                funcOP:"GET_FILE",
                data:{
                    Id: script.ID,
                    Filetype: "SCRIPT", //default of STDOUT
                    FP: 0
                }
            },

        }
      }).then((res) => {
        setShowScriptData(res.data.entry);
      }).catch((res) =>{
        alert(console.log(res))
      })
    }
    function Delete()
    {
        console.log("script deleted!");

        let text = document.getElementById("SelectScript");
        if (text.textContent !== "") {
            axios.post("/api", {
                body: {
                  op: "MANAGE_SCRIPTS",
                  data:{
                    funcOP: "DEL",
                    data: {
                        Id: selectedScript.ID
                    }
                  }
                }
                }).then((res) => {
                    setNumScripts(list.length - 1);
                  console.log(res.data)
                }).catch((res) =>{
                  alert("Post Failed")
                })
            
            closeDeleteScript();
        }
    }

    function Add(name, fname, desc, isAdmin, data)
    {
        console.log(name, fname, desc, isAdmin, data)
        
        axios.post("/api", {
            body: {
              op: "MANAGE_SCRIPTS",
              data: {
                funcOP: "ADD",
                data: {
                  Name: name,
                  fileName: fname,
                  Desc: desc,
                  isAdmin: isAdmin,
                  scriptData: data

                }
              }  
            }
        }).then((res) => {
            setNumScripts(list.length + 1)
            alert(name + " Script added")
        }).catch((res) =>{
            alert("Post Failed")
        })
        
        closeAddScript();
    }

    function Edit(id, name, fname, desc, admin, data) {
        let text = document.getElementById("SelectScript");
        if (text.textContent !== "") {
          axios.post("/api", {
            body: {
              op: "MANAGE_SCRIPTS",
              data: {
                  funcOP: "EDIT",
                  data: {
                      Id: id,
                      Name: name,
                      fileName: fname,
                      Desc: desc,
                      isAdmin: admin,
                      scriptData: data
                  }
              }
            }
          }).then((res) => {
            alert(JSON.stringify(res.data))
            setNumScripts(list.length + 0)
            //console.log(list)
          }).catch((res) =>{
            alert("Post Failed")
          })
          closeEditScript();
        }
    }


    function closeAddScript(){
        setShowAddScript(!showAddScript);
    }

    function closeDeleteScript(){
        setShowDeleteScript(!showDeleteScript);
    }

    function closeEditScript(){
        setShowEditScript(!showEditScript);
    }

    function Select_script(prams)
    {
        setSelectedScript(prams);
        showScript(prams);
    }
}

export default ScriptViewpage
