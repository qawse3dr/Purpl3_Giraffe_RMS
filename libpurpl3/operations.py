from flask import jsonify
import libpurpl3.preferences as pref 

def runScripts(data: dict) -> str:

  
  return jsonify(
    Error = pref.Success.toJson(),
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
