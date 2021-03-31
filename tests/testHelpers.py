import libpurpl3.preferences as pref
import libpurpl3.sshServer as ssh
import libpurpl3.tableOpComputer as computerTable
import libpurpl3.tableOpScript as scriptTable
import libpurpl3.tableOpScriptLog as scriptLogTable
import libpurpl3.tableOpUser as userTable
from Purpl3_RMS import app
import datetime
import unittest
import hashlib

'''
Helpers for unit testing application
'''

def createMockDB():
  '''
  creates a db for unit test
  saved in the file tests/res/unittest.db
  '''
  
  pref.setAttr(pref.CONFIG_DB_PATH,"tests/res/unittest.db")
  scriptLogTable.ScriptLogTable.createTable()
  scriptTable.ScriptTable.createTable()
  computerTable.ComputerTable.createTable()
  userTable.UserTable.createTable()

def clearDB():
  pref.setAttr(pref.CONFIG_DB_PATH,"tests/res/unittest.db")
  scriptLogTable.ScriptLogTable.deleteTable()
  scriptTable.ScriptTable.deleteTable()
  computerTable.ComputerTable.deleteTable()
  userTable.UserTable.deleteTable()
  
def createUserAccount():
  password = hashlib.sha256("unittest".encode()).hexdigest()
  entry = userTable.UserTable.createEntry("unittest",password,False)
  userTable.UserTable.add(entry)
  return entry

def createScript():
  entry =scriptTable.ScriptTable.createEntry("unittest","sleepScript.sh",1,"unittest script",False)
  scriptTable.ScriptTable.add(entry)
  return entry

def createComputer():
  entry = computerTable.ComputerTable.createEntry(1,"name","name","desc","root","localhost",False)
  computerTable.ComputerTable.add(entry)

  return entry

def mockApp() -> app.test_client_class:
  pref.setAttr(pref.CONFIG_SCRIPT_PATH,"tests/res/data/scripts/")
  pref.setAttr(pref.CONFIG_SCRIPT_LOG_PATH,"tests/res/data/scriptLogs/")

  c = app.test_client()
  with c.session_transaction() as sess:
    sess[pref.getNoCheck(pref.REQ_VAR_USER_ID)] = 1
  return c
