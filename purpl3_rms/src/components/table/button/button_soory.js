import './button.css'

const Button = (props) => {
    const onClick = () => {
        props.func(props)
        //console.log(props.name)
    }
    return (
        <div>
            <button className="tableButton" onClick={onClick} scriptid={props.scriptid}>{props.name}</button>
        </div>
    )
}


export default Button
