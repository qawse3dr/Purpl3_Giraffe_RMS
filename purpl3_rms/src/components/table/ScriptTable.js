import './table.css'
import Button from './button/button_soory.js';

const Table = (props) => {
    function addButtons(params) {
        let output = params.map((item, i)=> <Button key={i} scriptid={item.ID} index={i} name={item.name} func={props.func}/>)
        return <div>{output}</div>
    }

    return (
        <div id="table">
            {addButtons(props.input)}
        </div>
    )
}

export default Table
