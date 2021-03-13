import logging
from flask import jsonify
import libpurpl3.preferences as pref 
import libpurpl3.sshServer as ssh
import libpurpl3.tableOpComputer as computerTable
import libpurpl3.tableOpScript as scriptTable
import libpurpl3.tableOpUser as userTable


#Creates logger
logger = logging.getLogger("purpl3_rms")

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

    err, computer = computerTable.ComputerTable.getByID(scriptID)
    if(err != pref.Success):
      break

    err, script = scriptTable.ScriptTable.getByID(computerID)
    if(err != pref.Success):
      break
    #TODO change onces usersessions are ready
    user = None
    
    #TODO remove once db is up
    computer.username = "larry"
    computer.IP = 'localhost'
    #Create ssh connection
    conn = ssh.sshConnection(computer,user,script)

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
  return jsonify(
    Error = pref.Success.toJson(),
    data = {
      "Success": True
    }
  )

def manageComputers(data: dict) -> str:

  return jsonify(
    Error = pref.Success.toJson(),
    data = {
      "Success": True
    }
  )

def manageScriptLogs(data: dict) -> str:
  return jsonify(
    Error = pref.Success.toJson(),
    data = {
      "Success": True
    }
  )

def scheduleScript(data: dict) -> str:
  return jsonify(
    Error = pref.Success.toJson(),
    data = {
      "Success": True
    }
  )
