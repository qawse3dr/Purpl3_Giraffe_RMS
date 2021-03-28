import logging
from flask import jsonify, session
import libpurpl3.preferences as pref 
import libpurpl3.sshServer as ssh
import libpurpl3.tableOp as tableOp
import libpurpl3.tableOpComputer as computerTable
import libpurpl3.tableOpScript as scriptTable
import libpurpl3.tableOpScriptLog as scriptLogTable
import libpurpl3.tableOpUser as userTable
import libpurpl3.tableReqHelpers as tableReqHelpers


#Creates logger
logger = logging.getLogger()

def runScripts(data: dict) -> str:
  '''
  @param data from frontend
  With is take in data from a post given by react frontend,
  and run a script based on the data
  Request:
  {
    ScriptID: <scriptId:int>
    ComputerId: <computerId:int>
  }
  Return
  {
    errorCode:{
        "code":int,
        “reason”:string
    },
    Id: int
  }
  '''

  #Error code of the call
  err = pref.Success
  scriptLogID = -1
  scriptID = -1
  computerID = -1
  for _ in range(1):

    #get names of objects
    scriptIDName = pref.getNoCheck(pref.REQ_VAR_SCRIPT_ID)
    computerIDName = pref.getNoCheck(pref.REQ_VAR_COMPUTER_ID)

    #get attributes
    try:
      scriptID = data[scriptIDName]
      computerID = data[computerIDName]
    except:
      err = pref.getError(pref.ERROR_INVALID_REQUEST,args=(data))
      logger.error(err)
      break

    err, computer = computerTable.ComputerTable.getByID(computerID)
    if(err != pref.Success):
      break

    err, script = scriptTable.ScriptTable.getByID(scriptID)
    if(err != pref.Success):
      break

    
    #Makes sure user is logged in
    userID = None
    try:
      userID = session[pref.getNoCheck(pref.REQ_VAR_USER_ID)]
    except:
      err = pref.getError(pref.ERROR_NOT_LOGGED_IN)
      break

    #Create ssh connection
    conn = ssh.sshConnection(computer, userID, script)

    #Connect to computer
    err = conn.connect()

    #Failed to connect
    if(err != pref.Success):
      break
    
    #Run program
    err, scriptLogID = conn.run()

    if(err != pref.Success):
      break
    
  #check if it connected
  return jsonify(
    Error = err.toJson(),
    Id = scriptLogID
  )


def manageScripts(data: dict) -> str:

  logger.info("Processing Manage Script Request")
  
  #Get vars names
  tableName = pref.getNoCheck(pref.TABLE_SCRIPT)

  #Convert to general request
  jsonData = manageTable(tableName, data)

  return jsonData

def manageComputers(data: dict) -> str:

  logger.info("Processing Manage Computer Request")

  #Get vars names
  tableName = pref.getNoCheck(pref.TABLE_COMPUTER)

  #Convert to general request
  jsonData = manageTable(tableName, data)

  return jsonData

def manageScriptLogs(data: dict) -> str:

  logger.info("Processing Manage Script Log Request")

  #Get vars names
  tableName = pref.getNoCheck(pref.TABLE_SCRIPT_LOGS)

  #Convert to general request
  jsonData = manageTable(tableName, data)

  return jsonData

def scheduleScript(data: dict) -> str:
  return jsonify(
    Error = pref.Success.toJson(),
    data = {
      "Success": True
    }
  )


def manageTable(tableName: str, data: dict):
  err = pref.Success
  opName = pref.getNoCheck(pref.REQ_VAR_FUNC_OP)
  op = None
  opDataName = pref.getNoCheck(pref.REQ_VAR_DATA)
  opData = None
  #gets data from dict
  try:
    opData = data[opDataName]
    op = data[opName]
  except:
    err = pref.getError(pref.ERROR_INVALID_REQUEST, args=(data))
    logger.error(err)
  
  if(err == pref.Success):
    jsonData = tableReqHelpers.processRequest(tableName,op,opData)
  else:
    jsonData = jsonify(Error = err.toJson())

  return jsonData