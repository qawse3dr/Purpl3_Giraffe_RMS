import React from 'react'
import LiveOutput from '../components/LiveOutput.js'

class RunScripts extends React.Component {
	constructor() {
	    super();
	    this.state = {
	      currentTab: "Run Script"
	    }
  	}

    render() {
        return (
        	<div>
        		<h1>Run Scripts Tabs!</h1>
           		<p>Soory add yo shit here</p>
           		<LiveOutput script="Aids" computer="Monkey"/>
            </div>
        );
    }
}

export default RunScripts