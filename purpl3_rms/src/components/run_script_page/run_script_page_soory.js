import './run_script_page.css';
import axios from "axios";
import Table from '../table/table_soory.js';
import LiveOutput from './LiveOutput.js';

const RunScriptPage = (props) => {
    return (
        <div>
            <div className="body">
                <div className="column">
                    <h1>Select Computer</h1>
                    <div className="scroll">
                        <Table input={[{name:'soory\'s computer\tIp:123.1234.7777',script:Select_computer_func},{name:'tom\'s computer     Ip:123.1234.7777',script:Select_computer_func},{name:'jeary\'s computer     Ip:123.1234.7777',script:Select_computer_func}]}/>
                    </div>
                </div>

                <div className="column">
                    <h1>Select Script</h1>
                    <div className="scroll">
                        <Table input={[{name:'script_1',script:Select_script_func},{name:'diamond hands script',script:Select_script_func},{name:'monkey see monkey do',script:Select_script_func}]}/>
                    </div>
                </div>

                <p id="Select_Computer_text"></p>
                <p id="Select_Script_text"></p>
            </div>

            <footer>
                <div className="Run_Button">
                    <button type="button" onClick={Run_script}>Run Script</button>
                </div>
                
                <textarea id="Live_Output" readonly rows="6" cols="200">
                    Run a program to view it's output!
                </textarea>
            </footer>
        </div>
    )
}

function Select_computer_func(parms){
    let text = document.getElementById("Select_Computer_text");
    text.textContent = "Selected Computer : " + parms;
    text.value = parms;
}

function Select_script_func(parms){
    let text = document.getElementById("Select_Script_text");
    text.textContent = "Selected Script : " + parms;
    text.value = parms;
}

function Run_script(parms){
    let in_computer = document.getElementById("Select_Computer_text");
    let in_script = document.getElementById("Select_Script_text");

    axios.post("/api", {
        body: {
          op:"RUN_SCRIPT",
          data:{
            ScriptID: in_script.value,
            ComputerID: in_computer.value
          }
        }
    }).then((res) => {
        alert(JSON.stringify(res.data))
        let btn = document.getElementById("run_page_runbtn");
        btn.value = res.data;
        console.log(btn.value.Id);
    
        //Set the live output
        alert(res.data.id); //Julian Testing, you can remove this later
        setLiveOutput(res.data.id); //Call to set the live output.

    }).catch((res) =>{
        alert("Post Failed"); //Prob remove this final ver

        //Set the live output (error)
        document.getElementById("Live_Output").value = "Running the script failed. Try again";
    })

    //Call to backend to retrieve script output.
    function setLiveOutput(parms){
      axios.post("/api", {
        body: {
            op:"GET_FILE",
            data:{
                Id: parms,
                Filetype: "ENUM"
            }
        }
        }).then((res) => {
            alert(JSON.stringify(res.data))

            //Set the live output textarea
            document.getElementById("Live_Output").value = res.data.entry
        }).catch((res) =>{
            alert("Post Failed")
        })
    }
}
  

export default RunScriptPage
