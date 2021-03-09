from flask import Flask , redirect, request, jsonify
import logging
import libpurpl3.preferences as pref
import libpurpl3.login as login 


#Creates logger
logger = logging.getLogger("purpl3_rms")

#Creates application
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

#Load preferences #TODO change to command line arg
pref.setConfigFile("config.yaml")


#sets loggers level
logger.setLevel(pref.getNoCheck(pref.CONFIG_LOG_LEVEL))

login.encryptPassword("yeet", b'93fB_lc6JzlZQqh2ywiHCTyacWN1NQpCo3EORh_upiM=')



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
    op = "OPERATION:"+request.json["body"]["op"]
    data = request.json["body"]["data"]

    returnValue = None

    err, apiFtn = pref.get(op)
    if(err == pref.Success):
      returnValue = apiFtn(data)
    else:
      logger.error(err)
      returnValue = jsonify(
        Error = {
          "code":err.code,
          "str": str(err)
          },
        data = {}
      )
    return (returnValue,200)

@app.route(pref.getNoCheck(pref.CONFIG_LOGIN_ENDPOINT), methods=['POST'])
def loginRequest():
    print("login request: ", request.json)
    op = "LOGIN_OPERATIONS:"+request.json["body"]["op"]
    data = request.json["body"]["data"]

    returnValue = None

    err, loginFtn = pref.get(op)
    if(err == pref.Success):
      returnValue = loginFtn(data)
    else:
      logger.error(err)
      returnValue = jsonify(
        Error = {
          "code":err.code,
          "str": str(err)
          },
        data = {}
      )
    return (returnValue,200)

    
if __name__ == '__main__':
  err, port = pref.get(pref.CONFIG_PORT)
  if(err.code == 0):
    app.run(debug=True,port=port)
  else:
    logger.critical(err)


