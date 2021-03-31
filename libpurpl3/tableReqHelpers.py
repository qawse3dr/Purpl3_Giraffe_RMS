'''
This class contains helpers function for connecting the frontend to the
sql table functions
@author Larry (qawse3dr) Milne
'''

import logging
import os
from typing import Tuple
from flask import jsonify, session
import libpurpl3.preferences as pref 
import libpurpl3.tableOp as tableOp
import libpurpl3.tableOpComputer as computerTable
import libpurpl3.tableOpScript as scriptTable
import libpurpl3.tableOpScriptLog as scriptLogTable
import libpurpl3.tableOpUser as userTable
import libpurpl3.sshServer as ssh

#Creates logger
logger = logging.getLogger()

'''
retrives table class based on table name
'''


def processRequest(tableName: pref.prefENUM, tableOP: pref.prefENUM, data: dict):
  '''
  Completes a table request 
  @param tableName the name of the table from preferences ie pref.TABLE_COMPUTER, pref.TABLE_SCRIPT, pref.TABLE_SCRIPT_LOGS
  @param tableOp the operation of the script pref.TABLE_OP_GET_BY_ID, pref.TABLE_OP_ADD ....
  @param data request data from the tableOP
  @return jsonfiy value contiaining error and data
  '''
  #table classes dictionary linked to the preference value
  tableClasses = {
  pref.getNoCheck(pref.TABLE_SCRIPT): scriptTable.ScriptTable,
  pref.getNoCheck(pref.TABLE_SCRIPT_LOGS): scriptLogTable.ScriptLogTable,
  pref.getNoCheck(pref.TABLE_COMPUTER): computerTable.ComputerTable,
  }
  table = tableClasses[tableName]

  #Return value
  err = pref.Success
  returnVal = None
  

  #get file
  if(tableOP == pref.getNoCheck(pref.TABLE_OP_GET_FILE)):
    
    err = pref.Success

    #Gets id
    id = None
    Filetype = None
    FP = None
    try:
      id = data[pref.getNoCheck(pref.REQ_VAR_ID)]
      Filetype = data[pref.getNoCheck(pref.REQ_VAR_FILE_TYPE)]
      FP = data[pref.getNoCheck(pref.REQ_VAR_FP)]
    except: #Invalid request
      err = pref.getError(pref.ERROR_INVALID_REQUEST,args=(data))
      logger.error(err)
    
    #gets the element by id
    err, entry = table.getByID(id)

    if(err == pref.Success):
      #get file file
      if(Filetype == pref.getNoCheck(pref.REQ_VAR_FILE_STDOUT)):
        scriptPath = pref.getNoCheck(pref.CONFIG_SCRIPT_LOG_PATH)
        filename = scriptPath + entry.stdoutFile
      elif(Filetype == pref.getNoCheck(pref.REQ_VAR_FILE_STDERR)):
        scriptPath = pref.getNoCheck(pref.CONFIG_SCRIPT_LOG_PATH)
        filename = scriptPath +entry.stderrFile
      elif(Filetype == pref.getNoCheck(pref.REQ_VAR_FILE_SCRIPT)):
        scriptPath = pref.getNoCheck(pref.CONFIG_SCRIPT_PATH)
        filename = scriptPath + entry.fileName

      fp = open(filename,"r")
      fp.seek(FP,os.SEEK_SET)
      fileData = "".join(fp.readlines())
      newFP = fp.tell()

      returnVal = jsonify(Error = err.toJson(), entry=fileData,FP=newFP)

      
  #add to table
  elif(tableOP == pref.getNoCheck(pref.TABLE_OP_ADD)):
    
    err, entry = createObjFromReq(tableName, table, data)

    #Computer only used to add ssh key to computer
    if(err == pref.Success and tableName == pref.getNoCheck(pref.TABLE_COMPUTER)):
      try:
        username = data[pref.getNoCheck(pref.REQ_VAR_USERNAME)]
        password = data[pref.getNoCheck(pref.REQ_VAR_PASSWORD)]
        IP = data[pref.getNoCheck(pref.REQ_VAR_IP)]
      except:
        err = pref.getError(pref.ERROR_INVALID_REQUEST,args=(data))
        logger.error(err)

      #Add ssh key to computer uer password and username
      if(err == pref.Success):
        err = ssh.sshConnection.addNewComputer(IP, username,password)
    
    #add entry to table
    id = -1
    if(err == pref.Success):
      err = table.add(entry)
      if(err == pref.Success):
        id = entry.ID
    #return value
    
    returnVal = jsonify(Error = err.toJson(), Id = id)

  #delete from table
  elif(tableOP == pref.getNoCheck(pref.TABLE_OP_DEL)):
    id = None
    try:
      id = data[pref.getNoCheck(pref.REQ_VAR_ID)]

    except: #Invalid request
      err = pref.getError(pref.ERROR_INVALID_REQUEST,args=(data))
      logger.error(err)
    
    #Delete from table
    if(err == pref.Success):
      err = table.delete(id)
    returnVal = jsonify(Error=err.toJson())
  #remove from table
  elif(tableOP == pref.getNoCheck(pref.TABLE_OP_GET_ALL)):
    err, entries = table.getAll()

    entriesJson = []
    for entry in entries:
      entriesJson.append(entry.toJson())

    returnVal = jsonify(Error = err.toJson(), entries= entriesJson)

  #Get By ID
  elif(tableOP == pref.getNoCheck(pref.TABLE_OP_GET_BY_ID)):
    id = None
    try:
      id = data[pref.getNoCheck(pref.REQ_VAR_ID)]
    except: #TODO CREATE NEW ERROR
      err = pref.getError(pref.ERROR_INVALID_REQUEST,args=(data))

    #Gets the entry by id
    if(err == pref.Success):
      err, entry = table.getByID(id)

    #Creates return request
    entryResponse = None
    if(err == pref.Success): entryResponse = entry.toJson()
    returnVal = jsonify(Error=err.toJson(), entry=entryResponse)

  elif(tableOP == pref.getNoCheck(pref.TABLE_OP_EDIT)):
    err, entry = createObjFromReq(tableName, table, data)
    if(err == pref.Success):
      err = table.editEntry(entry)
    
    #create return object
    returnVal = jsonify(Error= err.toJson(), entry= entry.toJson())

  else: #This will never happen
    logger.warning("DIDN'T FIND TABLE REQUEST FAILED")
    err = pref.getError(pref.ERROR_INVALID_REQUEST,args=(data))
    returnVal = jsonify(Error= err.toJson())
  

  return returnVal
    
def createObjFromReq(tableName: str, table: tableOp.Table, data: dict) -> Tuple[pref.Error, tableOp.Entry]:
  '''
  creates a table object from a request data
  @param tableName the name of the table being use ie computer
  @param data tableData that the object will be created from
  @return newly created object
  '''
  entry = None
  err = pref.Success

  if(tableName == pref.getNoCheck(pref.TABLE_COMPUTER)):
    #computer table
    #vars
    userID = None
    nickName = None
    desc = None
    username = None
    IP = None
    asAdmin = None

    #run add computer script
    try:
      userID = session[pref.getNoCheck(pref.REQ_VAR_USER_ID)]
    except:
      err = pref.getError(pref.ERROR_NOT_LOGGED_IN)

    #Retrives data from request
    if(err == pref.Success):
      try:
        nickName = data[pref.getNoCheck(pref.REQ_VAR_NICK_NAME)]
        desc = data[pref.getNoCheck(pref.REQ_VAR_DESC)]
        username = data[pref.getNoCheck(pref.REQ_VAR_USERNAME)]
        IP = data[pref.getNoCheck(pref.REQ_VAR_IP)]
        asAdmin = data[pref.getNoCheck(pref.REQ_VAR_IS_ADMIN)]
      except:
        err = pref.getError(pref.ERROR_INVALID_REQUEST,args=(data))

    #create computer
    if(err == pref.Success):
      entry = computerTable.ComputerTable.createEntry(userID,None,nickName,desc,username,IP,asAdmin)

  elif(tableName == pref.getNoCheck(pref.TABLE_SCRIPT)):
    #script table
    name = None
    filename = None
    desc = None
    isAdmin = None
    scriptData = None
    userID = None

    err = pref.Success
    
    try:
      userID = session[pref.getNoCheck(pref.REQ_VAR_USER_ID)]
    except:
      err = pref.getError(pref.ERROR_NOT_LOGGED_IN)

    if(err == pref.Success):
      try:
          name = data[pref.getNoCheck(pref.REQ_VAR_NICK_NAME)]
          desc = data[pref.getNoCheck(pref.REQ_VAR_DESC)]
          filename = data[pref.getNoCheck(pref.REQ_VAR_FILE_NAME)]
          scriptData = data[pref.getNoCheck(pref.REQ_VAR_SCRIPT_DATA)]
          isAdmin = data[pref.getNoCheck(pref.REQ_VAR_IS_ADMIN)]
      except:
        err = pref.getError(pref.ERROR_INVALID_REQUEST,args=(data))

    #create file in script folder. return error if it already exists
    try:
      scriptPath = pref.getNoCheck(pref.CONFIG_SCRIPT_PATH)
      fp = open("{}{}".format(scriptPath,filename), "x")
      fp.write(scriptData)
    except:
      print("ere")
      err = pref.getError(pref.ERROR_CANT_CREATE_FILE, args=(name))


    #create computer
    if(err == pref.Success):
      entry = scriptTable.ScriptTable.createEntry(name,filename,userID,desc,isAdmin)

  return err, entry
