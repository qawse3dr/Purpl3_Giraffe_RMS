import './table.css'
import Button from './button/button_soory.js';

const Table = (props) => {
    return (
        <div id="table">
            {addButtons(props)}
        </div>
    )
}
function addButtons(params) {
    let output = params.input.map(item=> <Button key={item.name} name={item.name} func={item.script}/>)
    return <div>{output}</div>
}

export default Table
