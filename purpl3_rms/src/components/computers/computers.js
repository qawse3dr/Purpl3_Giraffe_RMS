import axios from "axios";
import ScriptTable from '../table/ScriptTable';
import React, {useState , useEffect} from "react";
import CreateComputer from './CreateComputer';
import DeleteComputer from './DeleteComputer';
import EditComputer from './EditComputer'

const ScriptViewpage = (props) => {
    const [numComputers, setNumComputers] = useState(0)
    const [list, setComputer_list] = useState([])
    const [showAddComputer, setShowAddComputer] = useState(false);
    const [selectedComputerID, setSelectedComputerID] = useState(0)
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
        <div>
            <h3>Select Computer</h3>
            <div className="scroll">
                <ScriptTable input={list} func={Select_computer}/>
            </div>
            
            <p id="SelectComputer"></p>
            <button style={{color:"blue"}} onClick={() => setShowEditComputer(!showEditComputer)}>Edit</button>
            <button style={{color:"red"}} onClick={() => setShowDeleteComputer(!showDeleteComputer)}>Delete</button>
            <button style={{color:"orange"}} onClick={() => setShowAddComputer(!showAddComputer)}>Create new computer +</button>
            {showAddComputer && <CreateComputer addComputer={Add} closeForm={closeAddComputer}/>}
            {showEditComputer && <EditComputer computerid={selectedComputerID} editComputer={Edit} closeForm={closeEditComputer}/>}
            {showDeleteComputer && <DeleteComputer deleteComputer={Delete} closeForm={closeDeleteComputer}/>}
        </div>
    );

    function Delete()
    {
        console.log("Computer deleted!");

        let text = document.getElementById("SelectComputer");
        console.log(text)
        if (text.textContent !== "") {
            axios.post("/api", {
                body: {
                  op: "MANAGE_COMPUTER",
                  data:{
                    funcOP: "DEL",
                    data: {
                        Id: selectedComputerID
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
            if(res.data.Error.code == 0){
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

        let text = document.getElementById("SelectComputer");
        if (text.textContent !== "") {
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
        setSelectedComputerID(prams.scriptid);
        let text = document.getElementById("SelectComputer");
        text.textContent = "Selected Computer : "+prams.name;
        text.value = prams.name;
        text.index = prams.index;
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

export default ScriptViewpage
