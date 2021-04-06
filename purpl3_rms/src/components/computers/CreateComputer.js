import React, {useState} from "react";
import './computers.css'

const CreateComputer = (props) => {

    const [name, setName] = useState('')
    const [description, setDescription] = useState('')
    const [admin, setAdmin] = useState(false)
    const [username, setUsername] = useState('')
    const [password, setPassword] = useState('')
    const [IP, setIP] = useState('')

    return (
        <div className="form-popup">
            <div className="form-content">
                <h2>Create New Computer</h2>

                <label for="name"><b>Name</b></label><br/>
                <input type="text"name="name" value={name} onChange={(e) => setName(e.target.value)}/><br/><br/>

                <label for="desc"><b>Description</b></label><br/>
                <input type="text" name="desc" value={description} onChange={(e) => setDescription(e.target.value)}/><br/><br/>

                <label for="username"><b>Username</b></label><br/>
                <input type="text" name="username" value={username} onChange={(e) => setUsername(e.target.value)}/><br/><br/>

                <label for="password"><b>Password</b></label><br/>
                <input type="password" name="password" value={password} onChange={(e) => setPassword(e.target.value)}/><br/><br/>

                <label for="IP"><b>IP</b></label><br/>
                <input type="text" name="IP" value={IP} onChange={(e) => setIP(e.target.value)}/><br/><br/>


                <label for="isAdmin"><b>Admin</b></label>
                <input type="checkbox" value={admin} onChange={(e) => setAdmin(e.currentTarget.checked)}></input><br/>


                <div className="button-container">
                    <button type="button" onClick={() => props.addComputer(name, description, username, password, IP, admin)} className="btn">Save</button>
                    <button type="button" className="btn" onClick={() => props.closeForm()} style={{backgroundColor: "#FF6347"}}>Cancel</button>
                </div>
            </div>
        </div>
    )


}

export default CreateComputer