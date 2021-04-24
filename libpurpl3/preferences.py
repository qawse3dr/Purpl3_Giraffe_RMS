'''
This will hold any all preference for the program
when interacting with this module ENUM should be use.
for example
```
import preferences as pref
pref.get(pref.CONFIG_PORT)
#instead of
pref.get("PORT")
#or (Please don't do this way)
pref.config("PORT")
```
'''


import logging
import copy
from typing import Any, Tuple, NewType
import yaml
from libpurpl3.errorCodes import *

#Creates logger
logger = logging.getLogger()

#create prefENUM datatype
prefENUM = NewType("prefENUM", str)

#Create config
CONFIG = None

def setConfigFile(filename: str) -> Error:
  '''
  sets the config file and overwrites value in current config.
  @param filename:string the path to the config file.
  @return success:bool if the file could be config or not #TODO change to error.
  '''
  
  try:
    global CONFIG
    oldConf = copy.deepcopy(CONFIG)
    err = Success
    logger.info("Using {} as config.".format(filename))
    with open(filename) as file:

      newConfig = yaml.load(file, Loader=yaml.FullLoader)
      
      for key in newConfig:
        if(key in CONFIG):
          logger.info("Preferences: {} found with value {}".format(key,newConfig[key]))
          CONFIG[key] = newConfig[key]
        else: #Attribute wasn't found revert changes
          err = getError(ERROR_ATTRIBUTE_NOT_FOUND,args=(key))
          logger.warning(err)
          CONFIG = oldConf
          break
  except IOError:
    logger.warning('Failed to open {} using default values'.format(filename))
    err = getError(ERROR_FILE_NOT_FOUND,args=(filename))
  except Exception as e: 
    err = getError(ERROR_UNKNOWN,args=(str(e)))
    logger.error(err)
  return err

def get(key: prefENUM) -> Tuple[Error, Any]:
  '''
  gets an attribute from preference manager from key.
  @param key ENUM/name of the attribute
  @return Error returns Success if no error as ocurred
  '''
  #No Error
  err = Success
  attribute = None

  try:
    #Checks if the error is inside another dict denoted by parent:child.
    if(':' in key):
      #Iterates though till tempConf is equal to the value at attribute.
      tempConfig = CONFIG
      for conf in key.split(":"):
        tempConfig = tempConfig[conf]

      #Set attribute to the final value.
      attribute = tempConfig

    else:
      #Value is not inside a dictionary just index the value.
      attribute = CONFIG[key]
  except LookupError: #error: couldn't find attribute.
    logger.warning("Attribute {} could not be found".format(key))
    err = getError(ERROR_ATTRIBUTE_NOT_FOUND, args=(key))

  except Exception as e: #error unknown error (shouldn't happen).
    err = getError(ERROR_UNKNOWN, args=(str(e)))
    logger.error(err)
  return err, attribute


def getNoCheck(key: prefENUM) -> Any:
  '''
  Gets an attribute without returning an error this should only be used
  if getAttr is used inline or you know the value will be there
  @see getAttribute for more info
  '''
  _, attr = get(key)
  return attr


def getError(key: prefENUM,args:Tuple = None ) -> Tuple[Error, Any]:
  '''
  Gets an error with the option to pass arguments when creating error.
  This should only be used for retriving errors.
  @param key the key of the error to be retrived.
  @param args any optional args that can be passed to an error @see error.extraArgs()
  @return a copy of the error.
  '''
  _, attr = get(key)
  err = copy.copy(attr)
  if(args != None):
    err.setExtraVars(args)
  return err

def errorToJson(error: Error):
  return {
          getNoCheck(ERROR_VAR_CODE):error.code,
          getNoCheck(ERROR_VAR_STR): str(error)
    }
setattr(Error, "toJson", errorToJson)

def setAttr(key: prefENUM, value: Any) -> Error:
  '''
  sets an new value to the attribute
  @param key ENUM/name of the attribute
  @param value the new value of the attribute
  @return Error returns Success if no error as ocurred
  '''
  #Assume the attribute doesn't exist till its found.
  err = getError(ERROR_ATTRIBUTE_NOT_FOUND, args=(key))


  #Get previous value. if the value doesn't exist return error.
  getAttrErr, _ = get(key)
  if(getAttrErr.code == 0):
    
    try:
      #Checks if the error is inside another dict denoted by parent:child.
      if(':' in key):

        #Get the attributes name (ERROR:SUCCESS would become SUCCESS).
        attrName = getAttrName(key)

        #Iterates though till conf is equal to the key.attrName.
        tempConfig = CONFIG
        for conf in key.split(":"):
          if(conf == attrName):
            logger.info("Attribute %s changed to %s" % (key, value))
            tempConfig[conf] = value
            #Attribute was set correctly.
            err = Success
          else:
            tempConfig = tempConfig[conf]

      else: #Value is not inside a dictionary just index the value.
        CONFIG[key] = value
        err = Success

    except LookupError: #error: couldn't find attribute.
      err = getError(ERROR_ATTRIBUTE_NOT_FOUND,args=(str(key)))
      logger.warning(err)

    except Exception as e: #unknown error.
      err = getError(ERROR_UNKNOWN,args=(str(e)))
      logger.error(err)
  else: #Attribute not found.
    err = getError(ERROR_ATTRIBUTE_NOT_FOUND,args=(key))
    logger.error(str(err))
  return err

'''
Constants used for referencing preferences.
These should always be used when interacting
with (get/set)Attribute to hardcoded values in our code.
'''
#general config
CONFIG_PORT = "PORT"
CONFIG_LOG_LEVEL = "LOG_LEVEL"
CONFIG_RES_FOLDER = "RES_FOLDER"
CONFIG_DB_PATH = "DB_PATH"

#endpoints
CONFIG_LOGIN_ENDPOINT = "LOGIN_ENDPOINT"
CONFIG_API_ENDPOINT = "API_ENDPOINT"
CONFIG_PING_ENDPOINT = "PING_ENDPOINT"

#Api operations
OPERATION_RUN_SCRIPT = "OPERATION:RUN_SCRIPT"
OPERATION_MANAGE_SCRIPT = "OPERATION:MANAGE_SCRIPTS"
OPERATION_MANAGE_COMPUTERS = "OPERATION:MANAGE_COMPUTER"
OPERATION_MANAGE_SCRIPT_LOGS = "OPERATION:MANAGE_SCRIPT_LOGS"
OPERATION_SCHEDULE_SCRIPT = "OPERATION:SCHEDULE_SCRIPTS"
OPERATION_GET_FILE = "OPERATION:" #Gets a file by type and id (type: "SCRIPT", id:10).

#SSH configs
CONFIG_PRIVATE_SSH_KEY = "PRIVATE_SSH_KEY_PATH"
CONFIG_PUBLIC_SSH_KEY = "PUBLIC_SSH_KEY_VALUE"
CONFIG_SCRIPT_PATH = "SCRIPT_PATH"
CONFIG_SCRIPT_LOG_PATH = "SCRIPT_LOG_PATH"
CONFIG_REMOTE_FOLDER = "REMOTE_FOLDER"
CONFIG_OUTPUT_TIMEOUT = "OUTPUT_TIMEOUT"

#Whitelist blacklist
CONFIG_BLACKLIST_CMD_FILE = "BLACKLIST_CMD_FILE"
CONFIG_BLACKLIST_IP_FILE  = "BLACKLIST_IP_FILE"

#session key for flask
CONFIG_SESSION_KEY = "SESSION_KEY"
#built in script names (will be assumed to be in res folder)
CONFIG_ADD_COMPUTER_SCRIPT = "ADD_COMPUTER_SCRIPT_NAME"

#Table types
TABLE_SCRIPT = "TABLE:SCRIPT"
TABLE_SCRIPT_LOGS = "TABLE:SCRIPT_LOGS"
TABLE_COMPUTER = "TABLE:COMPUTERS"

#table operations
TABLE_OP_GET_BY_ID = "TABLE_OP:GET_BY_ID"
TABLE_OP_GET_ALL = "TABLE_OP:GET_ALL"
TABLE_OP_ADD = "TABLE_OP:ADD"
TABLE_OP_DEL = "TABLE_OP:DEL"
TABLE_OP_EDIT = "TABLE_OP:EDIT"
TABLE_OP_GET_FILE = "TABLE_OP:GET_FILE"


#Login operations
LOGIN_LOGIN = "LOGIN:LOGIN"
LOGIN_RESET_PASSWORD = "LOGIN:RESET_PASSWORD"
LOGIN_CHANGE_PASSWORD = "LOGIN:CHANGE_PASSWORD"
LOGIN_USERNAME = "LOGIN:USERNAME"
LOGIN_PASSWORD = "LOGIN:PASSWORD"
LOGIN_LOGOUT = "LOGIN:LOGOUT"

#ErrorCodes dictionary of all error codes.
CONFIG_ERROR_CODES = "ERROR"

#Request vars for requests
REQ_VAR_BODY = "REQ_VAR:BODY"
REQ_VAR_DATA = "REQ_VAR:DATA"
REQ_VAR_OP   = "REQ_VAR:OP"
REQ_VAR_FUNC_OP   = "REQ_VAR:FUNC_OP"
REQ_VAR_SCRIPT_ID = "REQ_VAR:SCRIPT_ID"
REQ_VAR_COMPUTER_ID = "REQ_VAR:COMPUTER_ID"
REQ_VAR_USER_ID = "REQ_VAR:USER_ID"
REQ_VAR_NICK_NAME = "REQ_VAR:NICK_NAME"
REQ_VAR_DESC = "REQ_VAR:DESC"
REQ_VAR_USERNAME = "REQ_VAR:USERNAME"
REQ_VAR_PASSWORD = "REQ_VAR:PASSWORD"
REQ_VAR_IP = "REQ_VAR:IP"
REQ_VAR_IS_ADMIN = "REQ_VAR:IS_ADMIN"
REQ_VAR_ID = "REQ_VAR:ID"
REQ_VAR_FILE_TYPE = "REQ_VAR:FILE_TYPE"
REQ_VAR_FP = "REQ_VAR:FP"
REQ_VAR_FILE_STDOUT = "REQ_VAR:FILE_STDOUT"
REQ_VAR_FILE_STDERR = "REQ_VAR:FILE_STDERR"
REQ_VAR_FILE_SCRIPT = "REQ_VAR:FILE_SCRIPT"
REQ_VAR_FILE_NAME = "REQ_VAR:FILE_NAME"
REQ_VAR_SCRIPT_DATA = "REQ_VAR:SCRIPT_DATA"
CONFIG_OPERATIONS = "OPERATION"
def getOperationList() -> dict:
  '''
  @return dict of all operations.
  '''
  return {
    getAttrName(OPERATION_RUN_SCRIPT): "RUN_SCRIPT",
    getAttrName(OPERATION_MANAGE_SCRIPT): "MANAGE_SCRIPTS",
    getAttrName(OPERATION_MANAGE_COMPUTERS): "MANAGE_COMPUTER",
    getAttrName(OPERATION_MANAGE_SCRIPT_LOGS): "MANAGE_SCRIPT_LOGS",
    getAttrName(OPERATION_SCHEDULE_SCRIPT):  "SCHEDULE_SCRIPT",
  }


CONFIG_TABLE_OPERATION = "TABLE_OP"
def getTableOperationList() -> dict:
  '''
  @return dict of all tables operations.
  '''
  return {
    getAttrName(TABLE_OP_GET_BY_ID): "GET_BY_ID",
    getAttrName(TABLE_OP_GET_ALL): "GET_ALL",
    getAttrName(TABLE_OP_ADD): "ADD",
    getAttrName(TABLE_OP_DEL): "DEL",
    getAttrName(TABLE_OP_EDIT): "EDIT",
    getAttrName(TABLE_OP_GET_FILE): "GET_FILE"
  }

CONFIG_TABLES = "TABLE"
def getTableList() -> dict:
  '''
  @return dict of all tables.
  '''
  return {
    getAttrName(TABLE_SCRIPT): "SCRIPT_TABLE",
    getAttrName(TABLE_SCRIPT_LOGS): "SCRIPT_LOGS_TABLE",
    getAttrName(TABLE_COMPUTER): "COMPUTERS_TABLE",
  }

CONFIG_LOGIN_OPERATION = "LOGIN"
def getLoginOperations() -> dict:
  '''
  @return dict of all login table Operations.
  '''
  return {
    getAttrName(LOGIN_LOGIN): "LOGIN",
    getAttrName(LOGIN_LOGOUT): "LOGOUT",
    getAttrName(LOGIN_CHANGE_PASSWORD): "CHANGE_PASSWORD",
    getAttrName(LOGIN_RESET_PASSWORD): "RESET_PASSWORD",
    getAttrName(LOGIN_USERNAME): "Username",
    getAttrName(LOGIN_PASSWORD): "Password",
  }

CONFIG_REQUEST_VAR = "REQ_VAR"
def getRequestVars() -> dict:
  '''
  @return dict of all request vars ie "body".
  '''
  return {
    getAttrName(REQ_VAR_BODY) : "body",
    getAttrName(REQ_VAR_DATA) : "data",
    getAttrName(REQ_VAR_OP) : "op",
    getAttrName(REQ_VAR_FUNC_OP): "funcOP",
    getAttrName(REQ_VAR_SCRIPT_ID) : "ScriptID",
    getAttrName(REQ_VAR_COMPUTER_ID) : "ComputerID",
    getAttrName(REQ_VAR_USER_ID): "userID",
    getAttrName(REQ_VAR_NICK_NAME): "Name",
    getAttrName(REQ_VAR_DESC): "Desc",
    getAttrName(REQ_VAR_USERNAME): "Username",
    getAttrName(REQ_VAR_PASSWORD): "Password",
    getAttrName(REQ_VAR_IP): "IP",
    getAttrName(REQ_VAR_IS_ADMIN): "isAdmin",
    getAttrName(REQ_VAR_ID): "Id",
    getAttrName(REQ_VAR_FILE_TYPE): "Filetype",
    getAttrName(REQ_VAR_FP): "FP",
    getAttrName(REQ_VAR_FILE_STDOUT): "STDOUT",
    getAttrName(REQ_VAR_FILE_STDERR): "STDERR",
    getAttrName(REQ_VAR_FILE_SCRIPT): "SCRIPT",
    getAttrName(REQ_VAR_FILE_NAME): "fileName",
    getAttrName(REQ_VAR_SCRIPT_DATA): "scriptData",

  }
#Holds default config settings.
def defaultConfig() -> dict:
  '''
  @return dict of default configuration for preferences manager.
  '''
  return {
    #General config
    CONFIG_PORT : 8080,
    CONFIG_LOG_LEVEL : logging.INFO,
    CONFIG_RES_FOLDER: "res/",
    CONFIG_DB_PATH: "purpl3_rms.db",

    #Endpoints
    CONFIG_LOGIN_ENDPOINT: "/login",
    CONFIG_API_ENDPOINT: "/api",
    CONFIG_PING_ENDPOINT: "/ping",

    #dict of error codes.
    CONFIG_ERROR_CODES: getErrorCodeList(),

    #dict of all operations.
    CONFIG_OPERATIONS: getOperationList(),

    #dict of all tables.
    CONFIG_TABLES: getTableList(),

    #dict of all table operations.
    CONFIG_TABLE_OPERATION: getTableOperationList(),

    #dict of all table operations.
    CONFIG_LOGIN_OPERATION: getLoginOperations(),

    CONFIG_REQUEST_VAR: getRequestVars(),

    #ssh configs
    CONFIG_PRIVATE_SSH_KEY: "res/key",
    CONFIG_PUBLIC_SSH_KEY: "",
    CONFIG_SCRIPT_PATH: "data/scripts/",
    CONFIG_SCRIPT_LOG_PATH: "data/scriptLogs/",
    CONFIG_REMOTE_FOLDER: "/tmp/Purpl3_RMS",

    #Whitelist blacklist
    CONFIG_BLACKLIST_CMD_FILE: "res/blacklistCMD.txt",
    CONFIG_BLACKLIST_IP_FILE : "res/blacklistIP.txt",

    #built in script names (will be assumed to be in res folder)
    CONFIG_ADD_COMPUTER_SCRIPT: "addSSHKey.sh",

    #key for sessions
    CONFIG_SESSION_KEY: "key",

    #Timeout for live output
    CONFIG_OUTPUT_TIMEOUT: 3
  }

#Create config.
CONFIG = defaultConfig()

#Resets the config to its default values.
def resetConfig() -> dict:
  '''
  reset the preferences back to the default value.
  '''
  global CONFIG
  CONFIG = defaultConfig()
