import '../run_script_page/run_script_page.css';
import axios from "axios";
import Table from '../table/table_soory.js';
import React, {useState ,useRef, Component} from "react";
import ReactDOM, { render } from 'react-dom';

const ScriptViewpage = (props) => {
    var scriptList = [{name:'soory\'s computer\tIp:123.1234.7777',script:Select_script},{name:'tom\'s computer     Ip:123.1234.7777',script:Select_script},{name:'jeary\'s computer     Ip:123.1234.7777',script:Select_script}];
    const [list,setScript_list] = useState(scriptList)

    function Delete(prams)
    {
        let text = document.getElementById("SelectScript");
        if (text.textContent !== "") 
        {
            var newList2 = [...list]
            newList2.splice(text.index,1)
            setScript_list(old_list => newList2)
            text.textContent = ""
        }
    }

    function Add_script(prams)
    {
        var new_script = {name:"new stuff",script:Select_script}
        setScript_list(old_list => [...old_list,new_script]);
        console.log("open the add script tab stuff")
    }

    function Edit(prams)
    {
        let text = document.getElementById("SelectScript");
        if (text.textContent !== "") 
        {
            console.log(list[text.index],"open the add script tab stuff")
        }
    }

    return(
        <div>
            <h3>Select Script</h3>
            <div className="scroll">
                <Table input={list}/>
            </div>
            
            <p id="SelectScript"></p>
            <button style={{color:"blue"}} onClick={Edit}>Edit</button>
            <button style={{color:"red"}} onClick={Delete}>Delete</button>
            <button style={{color:"orange"}} onClick={Add_script}>Create new script +</button>
        </div>
    );
}

function Select_script(prams)
{
    let text = document.getElementById("SelectScript");
    text.textContent = "Selected Script : "+prams.name;
    text.value = prams.name;
    text.index = prams.index;
}


export default ScriptViewpage
