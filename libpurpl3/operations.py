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

    err, computer = computerTable.ComputerTable.getByID(computerID)
    if(err != pref.Success):
      break

    err, script = scriptTable.ScriptTable.getByID(scriptID)
    if(err != pref.Success):
      break
    #TODO change onces usersessions are ready
    user = None
    
    #TODO remove once db is up
    
    if computerID == 0:
      computer.username = "larry"
      computer.IP = 'localhost'
    elif computerID == 1:
      computer.username = "root"
      computer.IP = 'localhost'
    elif computerID == 2:
      computer.username = "pi"
      computer.IP = '192.168.100.146'
    else:
      computer.username = "larry"
      computer.IP = 'localhost'

    #temp scripts till db is done #TODO get rid when db is done
    if scriptID == 0:
      script.fileName = "sleepScript.sh"
    elif scriptID == 1:
      script.fileName = "updateComputerArch.sh"
    elif scriptID == 2:
      script.fileName = "backupHome.sh"
    elif scriptID == 3:
      script.fileName = "reboot.sh"
    elif scriptID == 4:
      script.fileName = "shutdown.sh"
    else:
      script.fileName = "sleepScript.sh"
    
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
  err = pref.Success
  return jsonify(
    Error = err.toJson(),
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

def confirmValidCommads(fileName: str, blackListedCommands: dict) -> str:
    '''
    This function is too check a given file for blacklisted commands as defined
    by the admin of the server
    @param str fileName, the name of the script NOT INCLUDING DIRECTORY
    @param dict blackListedCommands, a dictonary of blacklisted commands, all elements of dict will be treated as a string
    '''
    try:
        script = open("../data/scripts" + fileName, "r")
    except IOError:
        return jsonify(Error = pref.getError(pref.ERROR_FILE_NOT_FOUND), args=(fileName))
    
    for commands in blackListedCommands:
        if commands + " " in script:
            #return if blacklisted command is contained within script
            return jsonify(Error = pref.getError(pref.ERROR_BLACKLISTED_COMMAND, args=(commands)))
    #return if no blacklisted commands are found
    return jsonify(
    Error = pref.Success.toJson(),
    data = {
      "Success": True
    }
    )
    
