import React, {useState, useEffect} from "react";
import './computers.css'
import axios from "axios";

const EditComputer = (props) => {

  const [name, setName] = useState('')
  const [description, setDescription] = useState('')
  const [admin, setAdmin] = useState(false)
  const [username, setUsername] = useState('')
  const [IP, setIP] = useState('')

    useEffect(() => {
        axios.post("/api", {
            body: {
              op: "MANAGE_COMPUTER",
              data:{
                funcOP: "GET_BY_ID",
                data: {
                    Id: props.computerid
                }
              }
            }
            }).then((res) => {
            let entry = res.data.entry;
              alert(JSON.stringify(res.data.entry))
              setDescription(entry.desc);
              setName(entry.nickName);
              setUsername(entry.username);
              setIP(entry.IP);
              if((entry.asAdmin).localeCompare("True") == 0){
                setAdmin(true);
              }
              else{
                setAdmin(false);
              }
            }).catch((res) =>{
              alert("Post Failed")
            })
    }, [])

    return (
        <div className="form-popup">
            <div className="form-content">
                <h2>Edit Computer</h2>

                <label for="name"><b>Name</b></label><br/>
                <input type="text"name="name" value={name} onChange={(e) => setName(e.target.value)}/><br/><br/>

                <label for="desc"><b>Description</b></label><br/>
                <input type="text" name="desc" value={description} onChange={(e) => setDescription(e.target.value)}/><br/><br/>

                <label for="username"><b>Username</b></label><br/>
                <input type="text" name="username" value={username} onChange={(e) => setUsername(e.target.value)}/><br/><br/>

                <label for="IP"><b>IP</b></label><br/>
                <input type="text" name="IP" value={IP} onChange={(e) => setIP(e.target.value)}/><br/><br/>


                <label for="isAdmin"><b>Admin</b></label>
                <input type="checkbox" value={admin} onChange={(e) => setAdmin(e.currentTarget.checked)}></input><br/>

                <div className="button-container">
                    <button type="button" onClick={() => props.editComputer(props.computerid, name, description, username, IP, admin)} className="btn">Save</button>
                    <button type="button" className="btn" onClick={() => props.closeForm()} style={{backgroundColor: "#FF6347"}}>Cancel</button>
                </div>
            </div>
        </div>
    )


}

export default EditComputer