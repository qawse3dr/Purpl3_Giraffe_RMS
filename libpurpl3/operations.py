from flask import jsonify
import libpurpl3.preferences as pref 


def runScripts(data: dict) -> str:
  return jsonify(
    Error = {
          "code":pref.Success.code,
          "str": str(pref.Success)
          },
    data = {
      "Success": True
    }
  )


def manageScripts(data: dict) -> str:
  return jsonify(
    Error = {
          "code":pref.Success.code,
          "str": str(pref.Success)
          },
    data = {
      "Success": True
    }
  )

def manageComputers(data: dict) -> str:
  return jsonify(
    Error = {
          "code":pref.Success.code,
          "str": str(pref.Success)
          },
    data = {
      "Success": True
    }
  )

def manageScriptLogs(data: dict) -> str:
  return jsonify(
    Error = {
          "code":pref.Success.code,
          "str": str(pref.Success)
          },
    data = {
      "Success": True
    }
  )

def scheduleScript(data: dict) -> str:
  return jsonify(
    Error = {
          "code":pref.Success.code,
          "str": str(pref.Success)
          },
    data = {
      "Success": True
    }
  )

def getFile(data: dict) -> str:
  return jsonify(
    Error = {
          "code":pref.Success.code,
          "str": str(pref.Success)
          },
    data = {
      "Success": True
    }
  )