'''
This file is too handle the login and account managment for the webpage
Ver 0.01
09/03/2020
'''

from flask import jsonify, session
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
    userName = data[pref.getNoCheck(pref.LOGIN_USERNAME)]
    password = hashlib.sha256(data[pref.getNoCheck(pref.LOGIN_PASSWORD)].encode()).hexdigest()

    if " " in userName or ";" in userName:
        return jsonify(Error = pref.getError(pref.ERROR_USERNAME_INVALID).toJson())

    userID = tableLogin.UserTable.checkLogin(userName=userName, password=password)
    
    # ErrorCode = None
    if userID != -1:
        ErrorCode = pref.Success
        session["userID"] = userID
    else:
        ErrorCode = pref.getError(pref.ERROR_USER_AUTHENTICATION_ERROR, args=(userName))
    
    
    return jsonify(
        Error = ErrorCode.toJson()
    )
    
def logout(data: dict)-> str:
    if "userID" in session:
        session.pop("userID", None)

    return jsonify(
        Error = pref.Success.toJson()
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
