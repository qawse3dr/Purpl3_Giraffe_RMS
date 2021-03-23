import React from 'react'
import RunScriptPage from '../components/run_script_page/run_script_page_soory.js'
import LiveOutput from '../components/run_script_page/LiveOutput.js'

class RunScripts extends React.Component {
    render() {
    	let script = document.getElementById("Select_Computer_text");
        return (
        	<div>
            	<RunScriptPage/>
            </div>
        );
    }
}

export default RunScripts