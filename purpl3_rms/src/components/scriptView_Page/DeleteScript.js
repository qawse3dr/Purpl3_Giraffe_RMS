import './ScriptForm.css'

const DeleteScript = (props) => {   

    return (
        <div className="form-popup">
            <div className="form-content">
                <h2 style={{textAlign: "center"}}>Are you sure you want to delete this script?</h2>
            
                <div className="button-container">
                    <button type="button" onClick={() => props.deleteScript()} className="btn">Yes</button>
                    <button type="button" className="btn" onClick={props.closeForm} style={{backgroundColor: "#FF6347"}}>No</button>
                </div>
            </div>
        </div>
    )


}

export default DeleteScript