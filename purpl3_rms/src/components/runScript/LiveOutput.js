
import React from "react"
import { Tab, TabContent, Tabs } from 'react-bootstrap';
import "./LiveOutput.css"

const LiveOutput = (props) => {
    // FIXME - null issue
    // const handleLiveOutput = useCallback(event => {
    //     console.log("handling live output");
    //     console.log("consoleType: ", event)

    // }, []);

    return 	(
        <div className ={"LiveOutput "+ props.className}>
          <Tabs
              className = "bg-dark"
              variant="pills"
            //   onSelect={handleLiveOutput} FIXME - null issue
              onSelect={consoleType =>  { this.props.setConsoleType(consoleType)}}
              defaultActiveKey="STDOUT"
          >
              <Tab eventKey="STDOUT" title="STDOUT" tabClassName="h-100">
                  <TabContent className="h-100">
                      <textarea readonly className="bg-secondary text-white scriptOutput out" value={props.stdout}></textarea>
                      
                  </TabContent>
              </Tab>
              <Tab eventKey="STDERR" title="STDERR">
                  <TabContent className="h-100">
                  <textarea readonly className="bg-secondary text-white scriptOutput out"  value={props.stderr}></textarea>
                  </TabContent>
              </Tab>
                
          </Tabs>
	      </div>
    );

}


export default LiveOutput