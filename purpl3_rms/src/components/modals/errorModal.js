import "./errorModal.css";
import {Modal, Button, Alert} from "react-bootstrap";
import { useContext } from "react";
import { ErrorContext } from "../../context/errorContext";


const ErrorModal = (props) => {

    const [error, setError] = useContext(ErrorContext);


    return (
        <Modal 
            {...props}
            size="lg"
            show={props.show}
            aria-labelledby="contained-modal-title-vcenter"
            centered
            
        >
            <Modal.Header closeButton>
                <Modal.Title id="contained-modal-title-vcenter">
                    Error has occured
                </Modal.Title>
            </Modal.Header>

            <Modal.Body>
                <h4>Code: {error && error.code}</h4>
                <h4>{error && error.reason}</h4>

            </Modal.Body>
            
            <Modal.Footer>
                <Button onClick={props.onHide}>Close</Button>
            </Modal.Footer>
        </Modal>
    )
}

export {ErrorModal}