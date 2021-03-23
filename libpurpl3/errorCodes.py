'''
This file holds the definaion of all the error codes contained in
the applications. error codes should only be accessed by preferences manager
and never use hard coded values
errors with use the following format
ERROR:ENUM_NAME: Error(code,string)
To retrive errors use getError(str,args:Tuple = None) function
ex
  getError(pref.ERROR_UNKNOWN,args=(err))
  getError(pref.ERROR_SUCCESS)
'''


class Error():
  '''
  Error hold error code and string description of error
  use:
    getError(key: str,args:Tuple[Any] = None ) -> Tuple[Error, Any]
  to create errors
  ex
    getError(pref.ERROR_UNKNOWN,args=(err))
    getError(pref.ERROR_SUCCESS)
  '''
  code = None
  string = None
  extraVars = tuple()

  def __init__(self,code: int,string: str):
    self.code = code
    self.string = string

  def setExtraVars(self,extraVars) -> None:
    '''
      @param extraVars any extra var that is needed when printing the Error
      Sets extra values used in the output of the error
      ex if setExtraVars("test") is passed and its an unknown error (code 1)
      first %d is always the error code and does not need to be passed.
        unknown_err.str = "Returned: %d, an unknown error has occurred: %s"
      it will become:
        Returned 1, an unknown error has occurred: test
    '''
    self.extraVars = extraVars

  def toJson(self) -> dict:
    '''Returns the error code as a dict so it can be use
    in Flask.jsonfiy 
    @return returns dict error code in format
    {
       code: <code>
       reason: <str reason>
    }
    '''
    #NOTE this function is overwritten in preferences.py
  def __str__(self):
    if(not isinstance(self.extraVars,tuple)):
      self.extraVars = (self.extraVars,)
    return self.string  % ((self.code,) + self.extraVars)

  def __eq__(self, other):
    return self.code == other.code


#Used so get attribute isn't need everytime to create return 0
Success = Error(0,"Returned: %d, no error has occurred.")

def getAttrName(attr: str) -> str:
  '''
  @param attr the attribute that will be parsed.
  @return the name of the attribute.
  Returns the name of the attribute / how it will be saved in the config
  file. each level of the config file is denoted by and ':' thus the last value will
  be the attr's name
  ie
    ERROR:UNKNOWN
  returns
    UNKNOWN
  '''
  return attr.split(":")[-1]


def getErrorCodeList() -> dict:
  '''Returns a dictionatry with all the error codes
  @return dict of all error codes. This should only be used
  by preferences.py
  '''
  return {
    #0-30
    getAttrName(ERROR_SUCCESS): Success,
    getAttrName(ERROR_UNKNOWN): Error(1,"Returned: %d, an unknown error has occurred: %s"),
    
    getAttrName(ERROR_FILE_NOT_FOUND): Error(3,"Returned: %d, file %s was not found"),
    getAttrName(ERROR_CANT_CREATE_FILE): Error(4,"Returned: %d, file %s could not be created"),

    getAttrName(ERROR_INVALID_REQUEST): Error(10,"Returned: %d, invalid request %s"),

    getAttrName(ERROR_ATTRIBUTE_NOT_FOUND) : Error(20,"Returned: %d, Attribute %s could not be found."),

    getAttrName(ERROR_SQL_FAILURE): Error(21, "Skeleton message for SQL errors."),
    #31-45 account managment
    getAttrName(ERROR_USER_AUTHENTICATION_ERROR): Error(31, "Returned: %d, failed login for %s"),
    getAttrName(ERROR_USERNAME_INVALID): Error(32, "Return: %d, failed login due too invalid username"),

    #46-59 ssh errors
    getAttrName(ERROR_CONNECTION_FAILED): Error(46,"Returned: %d, Connection to %s@%s could not be made."),

    getAttrName(ERROR_CANT_FIND_SSH_KEY) : Error(49,"Returned %d: failed to find a valid ssh key at %s."),
    getAttrName(ERROR_SSH_AUTHENTICATION_FAILED) : Error(50,"Returned %d: failed authentication over ssh for %s@%s."),
    getAttrName(ERROR_EMPTY_SSH_PUBLIC_KEY): Error(51,"Returned %d: PUBLIC_SSH_KEY_VALUE config is empty"),
    getAttrName(ERROR_SSH_PERMISSION_DENIED): Error(52, "Returned %d: permission denied accessing: %s"),
    getAttrName(ERROR_SSH_FAILED_TO_EXECUTE_SCRIPT): Error(53, "Returned %d: failed to execute script: %s"),
    getAttrName(ERROR_SSH_SCRIPT_FAILED_WITH_ERROR_CODE): Error(54, "Returned %d: script failed with error code: %s"),
    getAttrName(ERROR_SSH_CONNECTION_LOST): Error(55,"Returned %d: Connection to remote computer %s@%s running script %s lost"),

    #James' blacklist commands
    getAttrName(ERROR_BLACKLISTED_COMMAND): Error(56, "Returned%d, script contained invalid command: %s"),
    #Vars for error codes
    getAttrName(ERROR_VAR) : {
      getAttrName(ERROR_VAR_CODE) : "code",
      getAttrName(ERROR_VAR_STR) : "reason",
    }
      

  }

#0-30
ERROR_SUCCESS = "ERROR:ERROR_SUCCESS"
ERROR_UNKNOWN = "ERROR:ERROR_UNKNOWN"

ERROR_FILE_NOT_FOUND = "ERROR:FILE_NOT_FOUND"
ERROR_CANT_CREATE_FILE = "ERROR:CANT_CREATE_FILE"

ERROR_INVALID_REQUEST = "ERROR:INVALID_REQUEST"

ERROR_ATTRIBUTE_NOT_FOUND = "ERROR:ATTRIBUTE_NOT_FOUND"

#31-45 account managment
ERROR_USER_AUTHENTICATION_ERROR = "ERROR:ERROR_USER_ATHENTICATION_ERROR"
ERROR_USERNAME_INVALID = "ERROR:INVALID_USERNAME"

#46-59 ssh errors
ERROR_CONNECTION_FAILED = "ERROR:CONNECTION_FAILED"

ERROR_CANT_FIND_SSH_KEY = "ERROR:CANT_FIND_SSH_KEY"
ERROR_SSH_AUTHENTICATION_FAILED = "ERROR:SSH_AUTHENTICATION_FAILED"
ERROR_EMPTY_SSH_PUBLIC_KEY = "ERROR:EMPTY_SSH_PUBLIC_KEY"
ERROR_SSH_PERMISSION_DENIED = "ERROR:SSH_PERMISSION_DENIED"
ERROR_SSH_FAILED_TO_EXECUTE_SCRIPT = "ERROR:SSH_FAILED_TO_EXECUTE_SCRIPT"
ERROR_SSH_SCRIPT_FAILED_WITH_ERROR_CODE = "ERROR:ERROR_SSH_SCRIPT_FAILED_WITH_ERROR_CODE"
ERROR_SSH_CONNECTION_LOST = "ERROR:ERROR_SSH_CONNECTION_LOST"

#James' blacklist commands
ERROR_BLACKLISTED_COMMAND = "ERROR:ERROR_BLACKLISTED_COMMAND"

ERROR_VAR = "ERROR:VAR"
ERROR_VAR_CODE = "ERROR:VAR:CODE"
ERROR_VAR_STR = "ERROR:VAR:STR"

ERROR_SQL_FAILURE = "ERROR:SQL_FAILURE"
