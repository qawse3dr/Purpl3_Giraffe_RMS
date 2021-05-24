import SelectTable from '../selectTable/selectTable';
import React, {useState , useEffect, useContext} from "react";
import {Table, Button, ButtonGroup} from "react-bootstrap";
import CreateScript from './createScript';
import DeleteScript from './deleteScript';
import EditScript from './editScript'
import {addScript, deleteScript, editScript, getAllScripts, getScriptFile} from "../../libpurpl3/purpl3API"
import {ErrorContext} from "../../context/errorContext";


const ScriptViewPage = (props) => {
    const [numScripts, setNumScripts] = useState(0)
    const [list, setScript_list] = useState([])
    const [showAddScript, setShowAddScript] = useState(false);
    const [selectedScript, setSelectedScript] = useState(null)
    const [showDeleteScript, setShowDeleteScript] = useState(false);
    const [showEditScript, setShowEditScript] = useState(false);
    const [showScriptData, setShowScriptData] = useState("");
    const [error, setError] = useContext(ErrorContext);
    
    useEffect(() => {
      getAllScripts().then(res => {
        setScript_list(res.data.entries)
      }).catch(setError)
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
      getScriptFile(script.ID, 0).then(res => {
        setShowScriptData(res.data.entry);
      })
    }
    function Delete()
    {
      console.log("script deleted!");
      if (selectedScript !== "") {
        deleteScript(selectedScript.ID).then(res => {
          setNumScripts(list.length - 1);
        })
          
        closeDeleteScript();
      }
    }

    function Add(name, fname, desc, isAdmin, data)
    {
        console.log(name, fname, desc, isAdmin, data)
        addScript(name, fname, desc, isAdmin, data).then(res => {
          setNumScripts(list.length + 1)
        })
        
        closeAddScript();
    }

    function Edit(id, name, fname, desc, admin, data) {
        if (selectedScript) {
          editScript(id, name, fname, desc, admin, data).then(res => {

            setNumScripts(list.length + 0)
          }).catch(setError);
          
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

export default ScriptViewPage
