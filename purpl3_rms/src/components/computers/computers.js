import SelectTable from '../selectTable/selectTable';
import React, {useState , useEffect, useContext} from "react";
import {Button, ButtonGroup, Table} from "react-bootstrap";
import CreateComputer from './CreateComputer';
import DeleteComputer from './DeleteComputer';
import EditComputer from './EditComputer';
import {ErrorContext} from "../../context/errorContext";

import {addComputer, getAllComputers, deleteComputer, editComputer} from "../../libpurpl3/purpl3API"

const ComputerPage = (props) => {
    const [numComputers, setNumComputers] = useState(0);
    const [list, setComputer_list] = useState([]);
    const [showAddComputer, setAddComputer] = useState(false);
    const [showDeleteComputer, setDeleteComputer] = useState(false);
    const [showEditComputer, setEditComputer] = useState(false);
    const [selectedComputer, setSelectedComputer] = useState(null);
    const [error, setError] = useContext(ErrorContext);

    useEffect(() => {
      getAllComputers().then(res => {
        for(let entry of res.data.entries){
          entry.name = entry.nickName;
        }
        setComputer_list(res.data.entries)
        console.log("no error")
      }).catch((res) => {
        setError(res);
      })
    }, [numComputers])
    
    return(
        <div className="computerViewerContainer">
          <div className="title text-center">
            <h3>
              Computer Viewer
            </h3>
          </div>
            <div className="scrollComputers">
                <SelectTable value={selectedComputer} tableName="computerTable"  input={list} onChange={Select_computer}/>
            </div>
            
          <div className="action-buttons">
            <ButtonGroup className="font-weight-bold">
              <Button onClick={() => {setEditComputer(true)}} className="font-weight-bolder" variant="primary">Edit</Button>
              <Button onClick={() => {setDeleteComputer(true)}}  className="font-weight-bolder" variant="danger">Delete</Button>
              <Button onClick={() => {setAddComputer(true)}} className="font-weight-bolder" variant="success">Create</Button>
            </ButtonGroup>
          </div>

          {(showAddComputer === true)  && <CreateComputer addComputer={Add} closeForm={closeAddComputer}/>}
          {(showEditComputer === true) && <EditComputer computerid={selectedComputer.ID} editComputer={Edit} closeForm={closeEditComputer}/>}
          {(showDeleteComputer === true) && <DeleteComputer deleteComputer={Delete} closeForm={closeDeleteComputer}/>}
      
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
                    Username
                  </th>
                  <th>
                    IP
                  </th>
                  <th>
                    Date Created
                  </th>
                  <th>
                    Date Modified
                  </th>
                  <th>
                    Admin Computer
                  </th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>
                    {selectedComputer != null ? selectedComputer.name : "Select A Computer"}
                  </td>
                  <td>
                    {selectedComputer != null ? selectedComputer.desc : ""}
                  </td>
                  <td>
                    {selectedComputer != null ? selectedComputer.username : ""}
                  </td>
                  <td>
                    {selectedComputer != null ? selectedComputer.IP : ""}
                  </td>
                  <td>
                    {selectedComputer != null ? selectedComputer.dtCreated : ""}
                  </td>
                  <td>
                    {selectedComputer != null ? selectedComputer.dtModified : ""}
                  </td>
                  <td>
                    {selectedComputer != null ? selectedComputer.asAdmin : ""}
                  </td>
                </tr>
              </tbody>
            </Table>
        </div>
    );

    function Delete()
    {
        if (selectedComputer !== null) {
          deleteComputer(selectedComputer.ID).then(res =>{
            setNumComputers(numComputers-1);
            console.log(res.data)
          }).catch(setError);

          closeDeleteComputer();
        }
    }

    function Add(name, description, username, password, IP, admin)
    {        
      addComputer(name, description, username, password, IP, admin, (res) => {
        console.log(res)
        setNumComputers(list.length + 1)
        alert(name + " Script added")
      })
        
      closeAddComputer();
    }

    function Edit(id, name, description, username, IP, admin){
        if (selectedComputer !== null) {
          editComputer(id, name, description, username, IP, admin).then(res =>{
            setNumComputers(numComputers + 0);
          }).catch(setError);
          
          closeEditComputer();
        }
    }

    function closeAddComputer(){
        setAddComputer(!showAddComputer);
    }

    function closeDeleteComputer(){
        setDeleteComputer(!showDeleteComputer);
    }

    function closeEditComputer(){
        setEditComputer(!showEditComputer);
    }

    function Select_computer(prams)
    {
      console.log(prams)
      setSelectedComputer(prams);
    }

}

export default ComputerPage
