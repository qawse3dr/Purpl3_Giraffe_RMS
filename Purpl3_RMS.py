from flask import Flask , redirect, request, jsonify
import logging
import libpurpl3.preferences as pref
import libpurpl3.login as login
import libpurpl3.operations as op 
import libpurpl3.sshServer as sshServer

#Creates logger
logger = logging.getLogger("purpl3_rms")

#Creates application
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

#Load preferences #TODO change to command line arg
pref.setConfigFile("config.yaml")


#sets loggers level
logger.setLevel(pref.getNoCheck(pref.CONFIG_LOG_LEVEL))


#Functions for login and operations
LOGIN_OPS = {
  pref.getNoCheck(pref.LOGIN_LOGIN): login.login,
  pref.getNoCheck(pref.LOGIN_CHANGE_PASSWORD): login.changePassword,
  pref.getNoCheck(pref.LOGIN_RESET_PASSWORD): login.resetPassword,
}

OPS = {
  pref.getNoCheck(pref.OPERATION_RUN_SCRIPT): op.runScripts,
  pref.getNoCheck(pref.OPERATION_MANAGE_SCRIPT): op.manageScripts,
  pref.getNoCheck(pref.OPERATION_MANAGE_COMPUTERS): op.manageComputers,
  pref.getNoCheck(pref.OPERATION_MANAGE_SCRIPT_LOGS): op.manageScriptLogs,
  pref.getNoCheck(pref.OPERATION_SCHEDULE_SCRIPT): op.scheduleScript,
}



@app.route(pref.getNoCheck(pref.CONFIG_PING_ENDPOINT), methods=['POST'])
def ping():
    '''
    API Request /ping
    Used for testing connection from the backend to the frontend.
    request:
      {
        ping:ping
      }
    return:
      {
        ping:pong
      }
    '''
    print("ping request: ", request.json)
    return (jsonify(ping="pong"),200)

@app.route(pref.getNoCheck(pref.CONFIG_API_ENDPOINT), methods=['POST'])
def apiRequest():
    '''
    API Request /api
    used for all operations between frontend and backend
      ie
        RUN_SCRIPT
        MANAGE_SCRIPT
        MANAGE_COMPUTERS
        MANAGE_SCRIPT_LOGS
        SCHEDULE_SCRIPT
        GET_FILE
    request:
      {
        op: <operation:string>
        data: <opData:dict>
      }
    return:
      {
        Error:
      }
    '''
    print("api request: ", request.json)

    err = pref.Success

    #names of request vars
    bodyName = pref.getNoCheck(pref.REQ_VAR_BODY)
    dataName = pref.getNoCheck(pref.REQ_VAR_DATA)
    jsonOpName = pref.getNoCheck(pref.REQ_VAR_OP)

    try:
      opName = pref.CONFIG_OPERATIONS + ":" + request.json[bodyName][jsonOpName]
      data = request.json[bodyName][dataName]
    except:
      err = pref.getError(pref.ERROR_INVALID_REQUEST, args=(request.json))
      logger.error(err)
      
    returnValue = None

    if(err == pref.Success):
      err, op = pref.get(opName)
    
    if(err == pref.Success):
      apiFtn = OPS[op]
      returnValue = apiFtn(data)
    else:
      logger.error(err)
      returnValue = jsonify(
        Error = err.toJson(),
        data = {}
      )
    return (returnValue,200)

@app.route(pref.getNoCheck(pref.CONFIG_LOGIN_ENDPOINT), methods=['POST'])
def loginRequest():
    print("login request: ", request.json)

    #names of request vars
    bodyName = pref.getNoCheck(pref.REQ_VAR_BODY)
    dataName = pref.getNoCheck(pref.REQ_VAR_DATA)
    jsonOpName = pref.getNoCheck(pref.REQ_VAR_OP)


    opName = pref.CONFIG_LOGIN_OPERATION + ":" + request.json[bodyName][jsonOpName]
    data = request.json[bodyName][dataName]

    
    returnValue = None

    err, op = pref.get(opName)
    if(err == pref.Success):
      loginFtn = LOGIN_OPS[op]
      returnValue = loginFtn(data)
    else:
      logger.error(err)
      returnValue = jsonify(
        Error = err.toJson(),
        data = {}
      )
    return (returnValue,200)

    
if __name__ == '__main__':
  err, port = pref.get(pref.CONFIG_PORT)
  if(err.code == 0):
    app.run(debug=True,port=port)
  else:
    logger.critical(err)


