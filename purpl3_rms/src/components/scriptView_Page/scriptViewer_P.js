import axios from "axios";
import ScriptTable from '../table/ScriptTable';
import React, {useState , useEffect} from "react";
import CreateScript from './CreateScript';
import DeleteScript from './DeleteScript';
import EditScript from './EditScript'

const ScriptViewpage = (props) => {
    const [numScripts, setNumScripts] = useState(0)
    const [list, setScript_list] = useState([])
    const [showAddScript, setShowAddScript] = useState(false);
    const [selectedScriptID, setSelectedScriptID] = useState(0)
    const [showDeleteScript, setShowDeleteScript] = useState(false);
    const [showEditScript, setShowEditScript] = useState(false);

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
            }).catch((res) =>{
              alert("Post Failed")
            })
    }, [numScripts])

    return(
        <div>
            <h3>Select Script</h3>
            <div className="scroll">
                <ScriptTable input={list} func={Select_script}/>
            </div>
            
            <p id="SelectScript"></p>
            <button style={{color:"blue"}} onClick={() => setShowEditScript(!showEditScript)}>Edit</button>
            <button style={{color:"red"}} onClick={() => setShowDeleteScript(!showDeleteScript)}>Delete</button>
            <button style={{color:"orange"}} onClick={() => setShowAddScript(!showAddScript)}>Create new script +</button>
            {showAddScript && <CreateScript addScript={Add} closeForm={closeAddScript}/>}
            {showEditScript && <EditScript scriptid={selectedScriptID} editScript={Edit} closeForm={closeEditScript}/>}
            {showDeleteScript && <DeleteScript deleteScript={Delete} closeForm={closeDeleteScript}/>}
        </div>
    );

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
                        Id: selectedScriptID
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
        setSelectedScriptID(prams.scriptid);
        let text = document.getElementById("SelectScript");
        text.textContent = "Selected Script : "+prams.name;
        text.value = prams.name;
        text.index = prams.index;
    }
}

export default ScriptViewpage
