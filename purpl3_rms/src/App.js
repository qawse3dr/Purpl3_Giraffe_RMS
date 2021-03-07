import logo from './logo.svg';
import './App.css';
import axios from "axios";

function App() {
  return (
    <div className="App">
      
      <button onClick={Ping}>
          Ping
      </button>
    </div>
  );
}

function Ping(){
  
  axios.post("/ping", {
    body: {ping:"ping"}
    }).then((res) => {
      alert(JSON.stringify(res.data))
    }).catch((res) =>{
      alert("Post Failed")
    })
}
export default App;
