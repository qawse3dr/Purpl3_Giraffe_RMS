from flask import jsonify
import libpurpl3.preferences as pref 
import libpurpl3.sshServer as ssh

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

  for _ in range(1):

    #TODO change to get values from database stub when complete
    #create mock objects
    computer = type('Computer', (object,), 
        {
          'ip' : 'localhost',
          'username': "larry"
        })

    user = type('User', (object,), {'propertyName' : 'propertyValue'})
    script = type('Script', (object,), {'propertyName' : 'propertyValue'})
    
    #Create ssh connection
    conn = ssh.sshConnection(computer,user,script)

    #Connect to computer
    err = conn.connect()

    #Failed to connect
    if(err != pref.Success):
      break
    
    #Run program
    err = conn.run()

    if(err != pref.Success):
      break
    
  #check if it connected
  return jsonify(
    Error = err.toJson(),
    data = {
      "Success": True
    }
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
