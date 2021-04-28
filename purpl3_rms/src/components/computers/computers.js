import axios from "axios";
import SelectTable from '../table/SelectTable';
import React, {useState , useEffect} from "react";
import {Button, ButtonGroup, Table} from "react-bootstrap";
import CreateComputer from './CreateComputer';
import DeleteComputer from './DeleteComputer';
import EditComputer from './EditComputer'

const ComputerViewer = (props) => {
    const [numComputers, setNumComputers] = useState(0)
    const [list, setComputer_list] = useState([])
    const [showAddComputer, setShowAddComputer] = useState(false);
    const [selectedComputer, setSelectedComputer] = useState(null)
    const [showDeleteComputer, setShowDeleteComputer] = useState(false);
    const [showEditComputer, setShowEditComputer] = useState(false);

    useEffect(() => {
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
              setComputer_list(res.data.entries)
            }).catch((res) =>{
              alert("Post Failed")
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
              <Button onClick={() => {setShowEditComputer(true)}} className="font-weight-bolder" variant="primary">Edit</Button>
              <Button onClick={() => {setShowDeleteComputer(true)}}  className="font-weight-bolder" variant="danger">Delete</Button>
              <Button onClick={() => {setShowAddComputer(true)}} className="font-weight-bolder" variant="success">Create</Button>
            </ButtonGroup>
          </div>

          {showAddComputer && <CreateComputer addComputer={Add} closeForm={closeAddComputer}/>}
          {showEditComputer && <EditComputer computerid={selectedComputer.ID} editComputer={Edit} closeForm={closeEditComputer}/>}
          {showDeleteComputer && <DeleteComputer deleteComputer={Delete} closeForm={closeDeleteComputer}/>}
      
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
        console.log("Computer deleted!");

        if (selectedComputer !== null) {
            axios.post("/api", {
                body: {
                  op: "MANAGE_COMPUTER",
                  data:{
                    funcOP: "DEL",
                    data: {
                        Id: selectedComputer.ID
                    }
                  }
                }
                }).then((res) => {
                  refreshList();
            
                  console.log(res.data)
                }).catch((res) =>{
                  alert("Post Failed")
                })
            
            closeDeleteComputer();
        }
    }

    function Add(name, description, username, password, IP, admin)
    {
        console.log(name, description, username, password, IP, admin)
        
        axios.post("/api", {
            body: {
              op: "MANAGE_COMPUTER",
              data: {
                funcOP: "ADD",
                data: {
                  Name: name,
                  Desc: description,
                  Username: username,
                  Password:  password,
                  IP: IP,
                  isAdmin: admin

                }
              }  
            }
        }).then((res) => {
            if(res.data.Error.code === 0){
              setNumComputers(list.length + 1)
              alert(name + " Script added")
            } 
            else{
              alert(JSON.stringify(res.data.Error))
            }
              
            
        }).catch((res) =>{
            alert("Post Failed")
        })
        
        closeAddComputer();
    }

    function Edit(id, name, description, username, IP, admin){
        console.log(name, description, username, IP, admin)

        
        if (selectedComputer !== null) {
          axios.post("/api", {
            body: {
              op: "MANAGE_COMPUTER",
              data: {
                  funcOP: "EDIT",
                  data: {
                      Id: id,
                      Name: name,
                      Desc: description,
                      Username: username,
                      IP: IP,
                      isAdmin: admin
                  }
              }
            }
          }).then((res) => {
            refreshList()
            console.log(list)
          }).catch((res) =>{
            alert("Post Failed")
          })
          closeEditComputer();
        }
    }


    function closeAddComputer(){
        setShowAddComputer(!showAddComputer);
    }

    function closeDeleteComputer(){
        setShowDeleteComputer(!showDeleteComputer);
    }

    function closeEditComputer(){
        setShowEditComputer(!showEditComputer);
    }

    function Select_computer(prams)
    {
      console.log(prams)
      setSelectedComputer(prams);
        
    }

    function refreshList(){
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
          setComputer_list(res.data.entries)
        }).catch((res) =>{
          alert("Post Failed")
        })
    }
}

export default ComputerViewer
