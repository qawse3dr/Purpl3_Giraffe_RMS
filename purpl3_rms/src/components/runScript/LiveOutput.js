
import React from "react"
import { Tab, TabContent, Tabs } from 'react-bootstrap';
import "./LiveOutput.css"

class LiveOutput extends React.Component {

    render() {
    	return 	(
            <div className ={"LiveOutput "+ this.props.className}>
              <Tabs
                  className = "bg-dark"
                  variant="pills"
                  onSelect={consoleType =>  { this.props.setConsoleType(consoleType)}}
                  defaultActiveKey="STDOUT"
              >
                  <Tab eventKey="STDOUT" title="STDOUT" tabClassName="h-100">
                      <TabContent className="h-100">
                          <textarea readonly className="bg-secondary text-white scriptOutput out" value={this.props.stdout}></textarea>
                          
                      </TabContent>
                  </Tab>

                  <Tab eventKey="STDERR" title="STDERR">
                      <TabContent className="h-100">
                      <textarea readonly className="bg-secondary text-white scriptOutput out"  value={this.props.stderr}></textarea>
                      </TabContent>
                  </Tab>
                    
              </Tabs>
	          </div>
        );
    }
}


export default LiveOutput