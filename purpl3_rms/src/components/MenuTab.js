import React from "react"

//Class that defines the menu tabs. Depending on the button clicked, will load a different "page".
class MenuTab extends React.Component {
  constructor() {
    super();
    this.state = {
      currentTab: "Run Script"
    }

    this.handleRunScript = this.handleRunScript.bind(this);
    this.handleScriptLogs = this.handleScriptLogs.bind(this);
    this.handleSchedule = this.handleSchedule.bind(this);
    this.handleScriptViewer = this.handleScriptViewer.bind(this);
    this.handleErrorDoc = this.handleErrorDoc.bind(this);
  }

  //Changes the state
  handleRunScript() {
    this.setState(state => ({
        currentTab: "Run Script"
    }));
  }

  handleScriptLogs() {
    this.setState(state => ({
        currentTab: "Script Logs"
    }));
  }

  handleSchedule() {
    this.setState(state => ({
        currentTab: "Schedule"
    }));
  }

  handleScriptViewer() {
    this.setState(state => ({
        currentTab: "Script Viewer"
    }));
  }

  handleErrorDoc() {
    this.setState(state => ({
        currentTab: "Error Doc"
    }));
  }

  render() {
    let tabs = <div>
                <button onClick={this.handleRunScript}>
                  Run Script
                </button>
                <button onClick={this.handleScriptLogs}>
                  Script Logs
                </button>
                <button onClick={this.handleSchedule}>
                  Schedule
                </button>
                <button onClick={this.handleScriptViewer}>
                  Script Viewer
                </button>
                <button onClick={this.handleErrorDoc}>
                  Error Doc
                </button>
              </div>

    

    let displayCurrentTab;
    if (this.state.currentTab == "Run Script") {
      displayCurrentTab =  <div>
                      <textarea readonly rows="4" cols="50">
                        Run a program to view output!
                      </textarea>
                    </div>
    }

    if (this.state.currentTab == "Script Logs") {
      displayCurrentTab = <p>Script Log shit goes here!</p>
    }

    if (this.state.currentTab == "Schedule") {
      displayCurrentTab = <p>Schedulessss!</p>
    }

    if (this.state.currentTab == "Script Viewer") {
      displayCurrentTab = <p>View da scripts</p>
    }

    if (this.state.currentTab == "Error Doc") {
      displayCurrentTab = <p>ERROR DOCSSS!</p>
    }

    return (
      <div>
        {tabs}
        {displayCurrentTab}
      </div>
    )
  }
}

export default MenuTab