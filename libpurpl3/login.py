from flask import jsonify
import libpurpl3.preferences as pref 

def login(data: dict) -> str:
  
  return jsonify(
    Error = {
          "code":pref.Success.code,
          "str": str(pref.Success)
          },
    data = {
      "Success": True
    }
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