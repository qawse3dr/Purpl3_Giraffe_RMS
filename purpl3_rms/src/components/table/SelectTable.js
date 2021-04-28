import './table.css'
import {ToggleButtonGroup, ToggleButton} from "react-bootstrap"

const SelectTable = (props) => {
    function addButtons(objectList) {

        let buttons = [];
        for(let object of objectList){
            buttons.push(<ToggleButton className="TableButton font-weight-bolder" variant="success" value={object}>{object.name} </ToggleButton>);
        }
        
        return buttons;
    }

    return (
        <div className="SelectTableScroll">
            <ToggleButtonGroup className="Table" name={props.tableName} value={props.value} type="radio" vertical="true" onChange={props.onChange}>
                {addButtons(props.input)}
            </ToggleButtonGroup>
        </div>
    )
}

export default SelectTable
