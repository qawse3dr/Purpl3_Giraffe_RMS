'''
This file is too handle the login and account managment for the webpage
Ver 0.01
09/03/2020
'''

from flask import jsonify, session, redirect
import hashlib
import flask as flask
import libpurpl3.preferences as pref
import libpurpl3.tableOpUser as tableLogin

#data[pref.getNoCheck(pref.LOGIN_USERNAME)]

#TODO add user sessions
def login(data: dict) -> str:
    '''
    This function is to handle the act of logging into the users account. 
    @param dict data, the dictonary of the users input data
    @return a json of the error code
    '''
    #makesure the prefs contain a username and password
    try:
        username = data[pref.getNoCheck(pref.LOGIN_USERNAME)]
        password = hashlib.sha256(data[pref.getNoCheck(pref.LOGIN_PASSWORD)].encode()).hexdigest()
    except:
        return jsonify(Error = pref.getError(pref.ERROR_ATTRIBUTE_NOT_FOUND).toJson())
    

    if " " in username or ";" in username:
        return jsonify(Error = pref.getError(pref.ERROR_USERNAME_INVALID).toJson())

    userID = tableLogin.UserTable.checkLogin(username=username, password=password)
    
    # ErrorCode = None
    if userID != -1:
        ErrorCode = pref.Success
        session["userID"] = userID
    else:
        ErrorCode = pref.getError(pref.ERROR_USER_AUTHENTICATION_ERROR, args=(username))
    
    
    return jsonify(
        Error = ErrorCode.toJson()
    )
    
def logout(data: dict)-> str:
    if "userID" in session:
        session.pop("userID", None)
        

    return jsonify(
        Error = pref.Success.toJson()
    )

def loginCheck(data: dict) -> str:
    '''
    Checks if the current session has anyone logged in
    '''
    err = pref.Success

    if not("userID" in session):
        err = pref.getError(pref.ERROR_NOT_LOGGED_IN)
    
    return jsonify(
        Error = err.toJson()
    )

def manageUser(data: dict) -> str:
    return jsonify(
        Error = {
            "code":pref.Success.code,
            "str": str(pref.Success)
            },
        data = {
        "Success": True
        }
    )

def changePassword(data: dict) -> str:
  return jsonify(
    Error = {
          "code":pref.Success.code,
          "str": str(pref.Success)
          },
    data = {
      "Success": True
    }
  )

def resetPassword(data: dict) -> str:
  return jsonify(
    Error = {
          "code":pref.Success.code,
          "str": str(pref.Success)
          },
    data = {
      "Success": True
    }
  )
