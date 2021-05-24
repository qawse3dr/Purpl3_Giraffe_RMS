import axios from "axios";

/**
 * @author Larry (qawse3dr) Milne
 * This file contains all backend calls wrapped in functions for 
 * 
 */

//operation type
const operations = Object.freeze({
  "scriptLogs": "MANAGE_SCRIPT_LOGS",
  "computer": "MANAGE_COMPUTER",
  "script": "MANAGE_SCRIPTS"
});

const filetypes = Object.freeze({
  "stdout": "STDOUT",
  "stderr": "STDERR",
  "script": "SCRIPT"
});

/**
 * 
 * @param {*} data validates script data
 * @returns "" if no error has occurred else will return the reason
 */
function validateScript(data){
  let reason = "";

  //description can be empty
  if(!data.Desc){
    data.Desc = "";
  }
  if(!data.scriptData){
    data.scriptData = "";
  }

  if(!data.Name){
    reason = createError(2,"Returned: 2, invalid Name.");
  
  } else if(!data.fileName || !data.fileName.includes(".")){
    reason = createError(2,"Returned: 2, invalid File Name.");
  
  } else if(typeof data.isAdmin !== "boolean"){
    reason = createError(2,"Returned: 2, invalid isAdmin.");
  }

  return reason;
}

/**
 * 
 * @param {*} data validates computer data
 * @returns "" if no error has occurred else will return the reason
 */
function validateComputer(data){
  let reason = "";

  if(!data.Desc){
    data.Desc = "";
  }
  if(!data.Password){
    data.Password = "";
  }

  if(!data.Name){
    reason = createError(2,"Returned: 2, invalid Name.");
  
  } else if(!data.Username){
    reason = createError(2,"Returned: 2, invalid Username.");
  
  } else if(!data.IP){
    reason = createError(2,"Returned: 2, invalid IP.");
  
  } else if(typeof data.isAdmin !== "boolean"){
    reason = createError(2,"Returned: 2, invalid isAdmin.");
  
  }
  return reason;
}

/**
 * 
 * @param {*} data validates id
 * @returns "" if no error has occurred else will return the reason
 */
function validateID(id){
  let reason = "";

  if(!Number.isInteger(Number(id)) || id < 1){
    reason = createError(2,"Returned: 2, invalid ID.");
  }
  return reason;
}

function createError(code, reason){
  return {
    code: code,
    reason: reason
  }
}
function handlePostSuccess(res, extraMessage, resolve, reject){
  if(res.data.Error.code === 0){
    resolve(res);
  } else{
    reject(res.data.Error)
  }
}

function handlePostFail(res, extraMessage, reject){
  reject(createError(5,"Returned: 5, Failed to connect to server"));
}

///////////////////////////////////////////////
//                                           //
//               GET_BY_ID                   //
//                                           //
///////////////////////////////////////////////


/**
 * 
 * @param {operation} operation operations type (operations.scriptLogs, operations.script, operations.computer)
 * @param {int} id id of the object being retrieved
 * @param {function(res)} callback function to be called after post request
 * @return  entry returned from operations throws error is any occurs
 */
function getEntryByID(operation, id, resolve, reject){

  let reason = validateID(id);
  if(reason){
    reject(reason)
    return
  } else {

    axios.post("/api", {
      body: {
        op: operation,
        data:{
          funcOP: "GET_BY_ID",
          data: {
            Id: id
          }
        }
      }
      }).then((res) => {
        handlePostSuccess(res, "", resolve, reject);
      }).catch((res) =>{
        handlePostFail(res, "", reject);
      })
  }
}

/**
 * 
 * @param {int} id id of the script being retrieved
 * @return  script returned from operations throws error is any occurs
 */
function getScriptByID(id){
  return new Promise((resolve, reject) => {
    //No Error checking unique to script id 
    getEntryByID(operations.script, id, resolve, reject);
  });
}

/**
 * 
 * @param {int} id id of the script logs being retrieved
 * @return  script logs returned from operations throws error is any occurs
 */
 function getScriptLogsByID(id){
  return new Promise((resolve, reject) => {
    //No Error checking unique to script log id
    getEntryByID(operations.scriptLogs, id, resolve, reject);
  });
}

/**
 * 
 * @param {int} id id of the script logs being retrieved
 * @return  script logs returned from operations throws error is any occurs
 */
 function getComputerByID(id){
  return new Promise((resolve, reject) => {
    //No Error checking unique to computer id  
    getEntryByID(operations.computer, id, resolve, reject);
  });
}

export {getScriptByID, getScriptLogsByID, getComputerByID};

///////////////////////////////////////////////
//                                           //
//               GET_ALL                     //
//                                           //
///////////////////////////////////////////////

/**
 * 
 * @param {operation} operation operations type (operations.scriptLogs, operations.script, operations.computer)
 * @param {function(res)} callback function to be called after post request
 * @return  entry returned from operations throws error is any occurs
 */
function getAllEntry(operation, resolve, reject){
  axios.post("/api", {
    body: {
      op: operation,
      data:{
        funcOP: "GET_ALL",
        data: {}
      }
    }
    }).then(res => {
      handlePostSuccess(res, "", resolve, reject);

    }).catch(res => {
      handlePostFail(res, "", reject);

    });
}

/**
 * 
 * @return  script returned from operations throws error is any occurs
 */
function getAllScripts(){
  return new Promise((resolve, reject) => {
    //No Error checking needed for GET_All 
    getAllEntry(operations.script, resolve, reject);
  })
}

/**
 * 
 * @return  script logs returned from operations throws error is any occurs
 */
 function getAllScriptLogs(){
  return new Promise((resolve, reject) => {
    //No Error checking needed for GET_All 
    getAllEntry(operations.scriptLogs, resolve, reject);
  })
}

/**
 * 
 * @param {function(res)} callback function to be called after post request
 * @return  script logs returned from operations throws error is any occurs
 */
 function getAllComputers(){
  return new Promise((resolve, reject) => {
    //No Error checking needed for GET_All 
    getAllEntry(operations.computer, resolve, reject);
  })
}

export {getAllScripts, getAllScriptLogs, getAllComputers};

///////////////////////////////////////////////
//                                           //
//                 ADD                       //
//                                           //
///////////////////////////////////////////////

/**
 * 
 * @param {operation} operation operations type (operations.scriptLogs, operations.script, operations.computer)
 * @param {int} id id of the object being retrieved
 * @param {function(res)} callback function to be called after post request
 * @return  entry returned from operations throws error is any occurs
 */
function addEntry(operation, data, resolve, reject){
  axios.post("/api", {
    body: {
      op: operation,
      data:{
        funcOP: "ADD",
        data: data
      }
    }
    }).then(res => {
      handlePostSuccess(res, "", resolve, reject);

    }).catch((res) =>{
      handlePostFail(res, "", reject);
    })
}

/**
 * 
 * @param {int} id id of the script being retrieved
 * @param {function(res)} callback function to be called after post request
 * @return  script returned from operations throws error is any occurs
 */
function addScript(Name, fileName, Desc, isAdmin, scriptData){
  
  return new Promise((resolve, reject) => {
    let data = {
      Name: Name,
      fileName: fileName,
      Desc: Desc,
      isAdmin: isAdmin,
      scriptData: scriptData
    }

    //Validate input
    let reason = validateScript(data);
    if(!reason) { //all checks passed
      addEntry(operations.script, data, resolve, reject);

    } else {
      reject(reason);
    }
  });
  
}

/**
 * 
 * @param {int} id id of the script logs being retrieved
 * @param {function(res)} callback function to be called after post request
 * @return  script logs returned from operations throws error is any occurs
 */
function addComputer(Name, Desc, Username, Password, IP, isAdmin){
  return new Promise((resolve, reject) => {
    let data = {
      Name: Name,
      Desc: Desc,
      Username: Username,
      Password: Password,
      IP: IP,
      isAdmin: isAdmin
    }

    //validate computer
    let reason = validateComputer(data);
    if(!reason){
      addEntry(operations.computer, data, resolve, reject);
    
    } else {
      reject(reason);
    }

  })
}

export {addScript, addComputer};

///////////////////////////////////////////////
//                                           //
//                 DEL                       //
//                                           //
///////////////////////////////////////////////

/**
 * 
 * @param {operation} operation operations type (operations.scriptLogs, operations.script, operations.computer)
 * @param {int} id id of the object being retrieved
 * @param {function(res)} callback function to be called after post request
 * @return  entry returned from operations throws error is any occurs
 */
function deleteEntry(operation, id, resolve, reject){
  let reason = validateID(id);
  if(reason){
    reject(reason)
    return
  } else{
    axios.post("/api", {
      body: {
        op: operation,
        data:{
          funcOP: "DEL",
          data: {
            Id: id
          }
        }
      }
      }).then(res => {
        handlePostSuccess(res,"", resolve, reject)    
  
      }).catch((res) =>{
        handlePostFail(res, "", reject)
      })
  }
}

/**
 * 
 * @param {int} id id of the script being retrieved
 * @param {function(res)} callback function to be called after post request
 * @return  script returned from operations throws error is any occurs
 */
function deleteScript(id){
  return new Promise((resolve, reject) => {
    //No Error checking unique to script id  
    deleteEntry(operations.script, id, resolve, reject);
  });
}

/**
 * 
 * @param {int} id id of the script logs being retrieved
 * @param {function(res)} callback function to be called after post request
 * @return  script logs returned from operations throws error is any occurs
 */
function deleteScriptLogs(id){
  return new Promise((resolve, reject) => {
    //No Error checking unique to script log id
    deleteEntry(operations.scriptLogs, id, resolve, reject);
  });
}

/**
 * 
 * @param {int} id id of the script logs being retrieved
 * @param {function(res)} callback function to be called after post request
 * @return  script logs returned from operations throws error is any occurs
 */
function deleteComputer(id){
  return new Promise((resolve, reject) => {
    //No Error checking unique to computer id  
    deleteEntry(operations.computer, id, resolve, reject);
  });
}

export {deleteScript, deleteScriptLogs, deleteComputer};

///////////////////////////////////////////////
//                                           //
//                 EDIT                      //
//                                           //
///////////////////////////////////////////////

/**
 * 
 * @param {operation} operation operations type (operations.scriptLogs, operations.script, operations.computer)
 * @param {int} id id of the object being retrieved
 * @param {function(res)} callback function to be called after post request
 * @return  entry returned from operations throws error is any occurs
 */
function editEntry(operation, data, resolve, reject){
  let reason = validateID(data.Id);
  if(reason){
    reject(reason)
    return
  } else {
    axios.post("/api", {
      body: {
        op: operation,
        data:{
          funcOP: "EDIT",
          data: data
        }
      }
      }).then(res => {
        handlePostSuccess(res, "", resolve, reject);
  
      }).catch((res) =>{
        handlePostFail(res, "", reject);
      })
  }
}

/**
 * 
 * @param {int} id id of the script being retrieved
 * @param {function(res)} callback function to be called after post request
 * @return  script returned from operations throws error is any occurs
 */
function editScript(Id, Name, fileName, Desc, isAdmin, scriptData){
  return new Promise((resolve, reject) => {
    let data = {
      Id: Id,
      Name: Name,
      fileName: fileName,
      Desc: Desc,
      isAdmin: isAdmin,
      scriptData: scriptData
    }

    //Validate input
    let reason = validateScript(data);
    if(!reason) { //all checks passed
      editEntry(operations.script, data, resolve, reject);

    } else {
      reject(reason);
    }
  });
}


/**
 * 
 * @param {int} id id of the script logs being retrieved
 * @param {function(res)} callback function to be called after post request
 * @return  script logs returned from operations throws error is any occurs
 */
function editComputer(Id, Name, Desc, Username, IP, isAdmin){
  return new Promise((resolve, reject) => {
    let data = {
      Id: Id,
      Name: Name,
      Desc: Desc,
      Username: Username,
      IP: IP,
      isAdmin: isAdmin
    }

    //validate computer
    let reason = validateComputer(data);
    if(!reason){
      editEntry(operations.computer, data, resolve, reject); 
    } else {
      reject(reason);
    }
  })
}

export {editScript, editComputer};

///////////////////////////////////////////////
//                                           //
//               GET_FILE                    //
//                                           //
///////////////////////////////////////////////

function getFile(operation, data, resolve, reject){
  let reason = validateID(data.Id);
  if(reason){
    reject(reason)
  } else {
    axios.post("/api", {
      body: {
        op: operation,
        data:{
          funcOP: "GET_FILE",
          data: data
        }
      }
      }).then(res => {
        handlePostSuccess(res, "", resolve, reject);
  
      }).catch((res) =>{
        console.log(res)
        handlePostFail(res, "", reject);
      })
  }


  
}

/**
 * 
 * @param {int} id id of the script being retrieved
 * @param {function(res)} callback function to be called after post request
 * @return  script returned from operations throws error is any occurs
 */
function getScriptFile(Id, FP){
  return new Promise((resolve, reject) => {
    let data = {
      Id:Id,
      Filetype: filetypes.script,
      FP: FP
    }

    //validate computer
    let reason = validateID(Id);
    if(!reason){
      getFile(operations.script, data, resolve, reject);
    } else {
      reject(reason);
    }
  })
}

/**
 * 
 * @param {int} id id of the script logs being retrieved
 * @param {function(res)} callback function to be called after post request
 * @return  script logs returned from operations throws error is any occurs
 */
function getScriptLogs(Id, FP, consoleType){
  return new Promise((resolve, reject) => {
    let data = {
      Id:Id,
      Filetype: consoleType,
      FP: FP
    }

    //validate computer
    let reason = validateID(Id);
    if(!reason){
      getFile(operations.scriptLogs, data, resolve, reject);
    } else {
      reject(reason);
    }
  })
}


export {getScriptLogs, getScriptFile};

///////////////////////////////////////////////
//                                           //
//              RUN_SCRIPT                   //
//                                           //
///////////////////////////////////////////////

function runScript(ScriptID, ComputerID){
  return new Promise((resolve, reject) =>{
    let reason = validateID(ScriptID);
    if(reason){
      reject(reason)
      return
    }
    reason = validateID(ComputerID);
    if(reason){
      reject(reason)
    } else {
      axios.post("/api", {
        body: {
          op: "RUN_SCRIPT",
          data:{
            ScriptID: ScriptID,
            ComputerID: ComputerID
          }
        }
        }).then(res => {
          handlePostSuccess(res, "", resolve, reject);
    
        }).catch((res) =>{
          handlePostFail(res, "", reject);
        })
    }
  });
}

export {runScript};


///////////////////////////////////////////////
//                                           //
//                   LOGIN                   //
//                                           //
///////////////////////////////////////////////

function loginRequest(username, password){
  return new Promise((resolve, reject) =>{
    if(!username || !password){
      let reason = createError(2, "Returned: 2, Invalid or empty username or password");
      reject(reason)
    } else {
      axios.post("/login", {
        body: {
            op: "LOGIN",
            data: {
                Username: username,
                Password: password
            }
          }
      }).then(res => {
        console.log(res)
          handlePostSuccess(res, "", resolve, reject);
    
      }).catch((res) =>{
          handlePostFail(res, "", reject);
      })
      
    }
  });
}

function logoutRequest(){
  return new Promise((resolve, reject) =>{
    axios.post("/login", {
      body: {
        op: "LOGOUT",
        data: {}
        }
    }).then(res => {
        handlePostSuccess(res, "", resolve, reject);
  
    }).catch((res) =>{
        handlePostFail(res, "", reject);
    }) 
  });
}

function loginCheckRequest(){
  return new Promise((resolve, reject) =>{
    axios.post("/login", {
      body: {
        op: "LOGIN_CHECK",
        data: {}
        }
    }).then(res => {
        if(res.data.Error.code === 0){
          resolve();
        }else{
          reject();
        }
  
    }).catch(() =>{
      reject();
    }) 
  });
}
export {loginRequest, logoutRequest, loginCheckRequest};


