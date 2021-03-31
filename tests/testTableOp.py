import libpurpl3.tableOp as to
import libpurpl3.tableOpScript as tos
import libpurpl3.tableOpScriptLog as tosl
import libpurpl3.tableOpComputer as toc
import libpurpl3.tableOpUser as tou
import libpurpl3.preferences as pref
import libpurpl3.sqlFuncs as sqlFuncs
import sqlite3
import datetime
from datetime import datetime as dt
import unittest
import os

def clearTables():
    '''
    Drops all SQL tables in database (scriptLog, script, computer and user)
    @param None.
    @return None.
    @Notes 
        All rows of a given table are deleted upon a drop table operation. 
        If any of these deletions trigger errors due to foreign key constraints or other issues, an error will be raised. 
        No error will be raised for dropping empty tables regardless of foreign key constraints on them.
    '''
    e = tosl.ScriptLogTable().deleteTable()
    e = tos.ScriptTable().deleteTable()
    e = toc.ComputerTable().deleteTable()
    e = tou.UserTable().deleteTable()

def createEmptyTables(): 
    '''
    Creates empty SQL tables for scriptLog, script, computer and user
    @param None.
    @return None.
    @Notes 
        Foreign key constraints are not checked when a table is created. 
        There is nothing stopping the user from creating a foreign key definition that refers 
            to a parent table that does not exist therefore creation order does not matter.
    '''
    clearTables()
    e = tosl.ScriptLogTable().createTable()
    e = tos.ScriptTable().createTable()
    e = toc.ComputerTable().createTable()
    e = tou.UserTable().createTable()

def createTables():
  '''
  Create tables (scriptLog, script, computer and user) with one record inserted into each of them
  @param None.
  @return None.
  '''
  createEmptyTables()
  # user entry 
  u = tou.UserTable().createEntry("rbroders", "hella_secure_hashed_password", True)
  err = tou.UserTable().add(u) # uID will be 1
  # script entry 
  s = tos.ScriptTable().createEntry("test_script_name", "test_script_name.sh", 1, "empty script used for testing", False)
  err = tos.ScriptTable().add(s)
  # computer entry 
  c = toc.ComputerTable().createEntry(1, "RachelsSurface", "Raquels Computer", "Rachel's wonderful awful computer", "rbroders", "idk how IPs are formatted ya yeet", False)
  err = toc.ComputerTable().add(c)
  # scriptLog entry
  sl = tosl.ScriptLogTable().createEntry(1, 1, 1, False)
  err = tosl.ScriptLogTable().add(sl)

def createTablesBig():
  '''
  Create tables (scriptLog, script, computer and user) with multiple records inserted into each of them
  @param None.
  @return None.
  '''
  createEmptyTables()
  # user entries
  u = tou.UserTable().createEntry("rbroders", "hella_secure_hashed_password", True)
  err = tou.UserTable().add(u) 
  u = tou.UserTable().createEntry("lmilne", "ya_yeet", False)
  err = tou.UserTable().add(u) 
  u = tou.UserTable().createEntry("jbusch", "beer-brand", True)
  err = tou.UserTable().add(u) 
  # script entries
  s = tos.ScriptTable().createEntry("test_script_name", "test_script_name.sh", 1, "empty script used for testing", False)
  err = tos.ScriptTable().add(s)
  s = tos.ScriptTable().createEntry("create_happiness", "reboot.sh", 1, "doggies and kitties", True)
  err = tos.ScriptTable().add(s)
  s = tos.ScriptTable().createEntry("solve_world_hunger", "shutdown.sh", 1, "crazy scritpt", False)
  err = tos.ScriptTable().add(s)
  s = tos.ScriptTable().createEntry("leprechan_script", "sleepScript.sh", 1, "found at end of rainbow", True)
  err = tos.ScriptTable().add(s)
  # computer entries 
  c = toc.ComputerTable().createEntry(1, "RachelsSurface", "Raquels Computer", "Rachel's wonderful awful computer", "rbroders", "idk how IPs are formatted ya yeet", False)
  err = toc.ComputerTable().add(c)
  c = toc.ComputerTable().createEntry(1, "Rachels Air", "Old computer", "dusty computer in closet", "rbroders22", "idk how IPs are formatted ya yeet... we can dream", True)
  err = toc.ComputerTable().add(c)
  c = toc.ComputerTable().createEntry(2, "Larry's Pi", "Raspberry Pie", "yum love pie", "lmilne", "idk how IPs are formatted ya yeet ... maybe one day", False)
  err = toc.ComputerTable().add(c)
  c = toc.ComputerTable().createEntry(3, "James' Computer", "JB Computer", "its a computer what can I say", "jbusch", "idk how IPs are formatted ya yeet...still", False)
  err = toc.ComputerTable().add(c)
  # scriptLog entries
  sl = tosl.ScriptLogTable().createEntry(1, 1, 3, False)
  err = tosl.ScriptLogTable().add(sl)
  sl = tosl.ScriptLogTable().createEntry(2, 2, 4, False)
  err = tosl.ScriptLogTable().add(sl)
  sl = tosl.ScriptLogTable().createEntry(3, 4, 2, False)
  err = tosl.ScriptLogTable().add(sl)
  sl = tosl.ScriptLogTable().createEntry(1, 3, 1, False)
  err = tosl.ScriptLogTable().add(sl)

def cleanUpCreateTables():
  clearTables()
  os.remove()

class BaseTestCase(unittest.TestCase):
    def setUp(self):
      pref.setAttr(pref.CONFIG_DB_PATH, "tests/res/unittest.db") # work on seperate clean database so as to not mess up test data in base db
      pref.setAttr(pref.CONFIG_SCRIPT_PATH,"tests/res/data/scripts/")
      pref.setAttr(pref.CONFIG_SCRIPT_LOG_PATH,"tests/res/data/scriptLogs/")

    ################## EDITENTRY TESTS (SUCCESS) ##################
    def test_editEntryS(self):
      createTablesBig()
      err, s = tos.ScriptTable().getByID(2)
      # change some of s's attribute
      s.name = "newName"
      s.fileName = "newFilename.sh"
      s.author = 1
      s.desc = "New desc"
      s.size = 200.0
      s.isAdmin = False
      s.dtModified = dt.now()
      # write these edits to table
      err, s2 = tos.ScriptTable().editEntry(s)
      errExp = pref.getError(pref.ERROR_SUCCESS)
      # checks
      self.assertEqual(err, errExp)
      self.assertEqual(s.ID, s2.ID)
      self.assertEqual(s.name, s2.name)
      self.assertEqual(s.fileName, s2.fileName)
      self.assertEqual(s.author, s2.author)
      self.assertEqual(s.desc, s2.desc)
      self.assertEqual(s.dtCreated, s2.dtCreated)
      self.assertEqual(s.dtModified, s2.dtModified)
      self.assertEqual(s.size, s2.size)
      self.assertEqual(s.isAdmin, s2.isAdmin)

    def test_editEntryC(self):
      createTablesBig()
      err, c = toc.ComputerTable().getByID(2)
      # change some of c's attribute
      c.userID = 2
      c.name = "newName"
      c.nickName = "newNickName"
      c.desc = "newDesc"
      c.username = "newUsername"
      c.IP = "newIP"
      c.dtModified = dt.now()
      c.asAdmin = True
      # write these edits to table
      err, c2 = toc.ComputerTable().editEntry(c)
      errExp = pref.getError(pref.ERROR_SUCCESS)
      # checks
      self.assertEqual(err, errExp)
      self.assertEqual(c.userID, c2.userID)
      self.assertEqual(c.name, c2.name)
      self.assertEqual(c.nickName, c2.nickName)
      self.assertEqual(c.desc, c2.desc)
      self.assertEqual(c.username, c2.username)
      self.assertEqual(c.IP, c2.IP)
      self.assertEqual(c.dtCreated, c2.dtCreated)
      self.assertEqual(c.dtModified, c2.dtModified)
      self.assertEqual(c.asAdmin, c2.asAdmin)

    def test_editEntrySL(self):
      createTablesBig()
      err, sl = tosl.ScriptLogTable().getByID(2)
      # change some of s's attribute
      sl.scriptID = 1
      sl.userID = 1
      sl.compID = 1
      sl.startTime = dt.now()
      sl.endTime = dt.now()
      sl.returnVal = -1
      sl.errorCode = 0
      sl.stdoutFile = "stdoutFile new"
      sl.stderrFile = "stderrFile new"
      sl.asAdmin = False
      # write these edits to table
      err, sl2 = tosl.ScriptLogTable().editEntry(sl)
      errExp = pref.getError(pref.ERROR_SUCCESS)
      # checks
      self.assertEqual(err, errExp)
      self.assertEqual(sl.ID, sl2.ID)
      self.assertEqual(sl.scriptID, sl.scriptID)
      self.assertEqual(sl.userID, sl.userID)
      self.assertEqual(sl.compID, sl.compID)
      self.assertEqual(sl.startTime, sl.startTime)
      self.assertEqual(sl.endTime, sl.endTime)
      self.assertEqual(sl.returnVal, sl.returnVal)
      self.assertEqual(sl.errorCode, sl.errorCode)
      self.assertEqual(sl.stdoutFile, sl.stdoutFile)
      self.assertEqual(sl.stderrFile, sl.stderrFile)
      self.assertEqual(sl.asAdmin, sl.asAdmin)

    def test_editEntryU(self):
      createTablesBig()
      err, u = tou.UserTable().getByID(2)
      # change some of s's attribute
      u.username = "new username"
      u.password = "new password"
      u.dtCreated = dt.now()

      # write these edits to table
      err, u2 = tou.UserTable().editEntry(u)
      errExp = pref.getError(pref.ERROR_SUCCESS)
      # checks
      self.assertEqual(err, errExp)
      self.assertEqual(u.username, u2.username)
      self.assertEqual(u.password, u2.password)
      self.assertEqual(u.dtCreated, u2.dtCreated)
      self.assertEqual(u.dtModified, u2.dtModified)
      self.assertEqual(u.admin, u2.admin)

    ################## EDITENTRY TESTS (FAILURE) ##################
    def test_editEntryS_F(self):
      createTablesBig()
      err, s = tos.ScriptTable().getByID(2)
      # change some of s's attribute
      s.ID = None
      # write these edits to table
      err, s2 = tos.ScriptTable().editEntry(s)
      errExp = pref.getError(pref.ERROR_NO_ID_PROVIDED, args=("editEntry", "Script"))
      # checks
      self.assertEqual(err, errExp)
      self.assertEqual(s.ID, s2.ID)
      self.assertEqual(s.name, s2.name)
      self.assertEqual(s.fileName, s2.fileName)
      self.assertEqual(s.author, s2.author)
      self.assertEqual(s.desc, s2.desc)
      self.assertEqual(s.dtCreated, s2.dtCreated)
      self.assertEqual(s.dtModified, s2.dtModified)
      self.assertEqual(s.size, s2.size)
      self.assertEqual(s.isAdmin, s2.isAdmin)

    def test_editEntryC_F(self):
      createTablesBig()
      err, c = toc.ComputerTable().getByID(2)
      # change some of c's attribute
      c.ID = None
      # write these edits to table
      err, c2 = toc.ComputerTable().editEntry(c)
      errExp = pref.getError(pref.ERROR_NO_ID_PROVIDED, args=("editEntry", "Computer"))
      # checks
      self.assertEqual(err, errExp)
      self.assertEqual(c.userID, c2.userID)
      self.assertEqual(c.name, c2.name)
      self.assertEqual(c.nickName, c2.nickName)
      self.assertEqual(c.desc, c2.desc)
      self.assertEqual(c.username, c2.username)
      self.assertEqual(c.IP, c2.IP)
      self.assertEqual(c.dtCreated, c2.dtCreated)
      self.assertEqual(c.dtModified, c2.dtModified)
      self.assertEqual(c.asAdmin, c2.asAdmin)

    def test_editEntrySL_F(self):
      createTablesBig()
      err, sl = tosl.ScriptLogTable().getByID(2)
      # change some of s's attribute
      sl.ID = None
      # write these edits to table
      err, sl2 = tosl.ScriptLogTable().editEntry(sl)
      errExp = pref.getError(pref.ERROR_NO_ID_PROVIDED, args=("editEntry", "ScriptLog"))
      self.assertEqual(err, errExp)
      self.assertEqual(sl.ID, sl2.ID)
      self.assertEqual(sl.scriptID, sl.scriptID)
      self.assertEqual(sl.userID, sl.userID)
      self.assertEqual(sl.compID, sl.compID)
      self.assertEqual(sl.startTime, sl.startTime)
      self.assertEqual(sl.endTime, sl.endTime)
      self.assertEqual(sl.returnVal, sl.returnVal)
      self.assertEqual(sl.errorCode, sl.errorCode)
      self.assertEqual(sl.stdoutFile, sl.stdoutFile)
      self.assertEqual(sl.stderrFile, sl.stderrFile)
      self.assertEqual(sl.asAdmin, sl.asAdmin)

    def test_editEntryU_F(self):
      createTablesBig()
      err, u = tou.UserTable().getByID(2)
      # change some of s's attribute
      u.ID = None
      # write these edits to table
      err, u2 = tou.UserTable().editEntry(u)
      errExp = pref.getError(pref.ERROR_NO_ID_PROVIDED, args=("editEntry", "User"))
      # checks
      self.assertEqual(err, errExp)
      self.assertEqual(u.ID, u2.ID)
      self.assertEqual(u.username, u2.username)
      self.assertEqual(u.password, u2.password)
      self.assertEqual(u.dtCreated, u2.dtCreated)
      self.assertEqual(u.dtModified, u2.dtModified)
      self.assertEqual(u.admin, u2.admin)

    ################## CREATE TABLE TESTS ##################
    # Tests table creation from user class directly (expecting success)
    def test_createTableU(self):
      clearTables()
      err = tou.UserTable().createTable()
      errExp = pref.getError(pref.ERROR_SUCCESS)
      self.assertEqual(err,errExp)

    # Tests table creation from script class directly (expecting success)
    def test_createTableS(self):
      clearTables()
      err = tos.ScriptTable().createTable()
      errExp = pref.getError(pref.ERROR_SUCCESS)
      self.assertEqual(err,errExp)

    # Tests table creation from computer class directly (expecting success)
    def test_createTableC(self):
      clearTables()
      err = toc.ComputerTable().createTable()
      errExp = pref.getError(pref.ERROR_SUCCESS)
      self.assertEqual(err,errExp)

    # Tests table creation from scriptLog class directly (expecting success)
    def test_createTableSL(self):
      clearTables()
      err = tosl.ScriptLogTable().createTable()
      errExp = pref.getError(pref.ERROR_SUCCESS)
      self.assertEqual(err,errExp)

    ################## DELETE EMPTY TABLE TESTS (SUCCESS) ##################
    # Tests deleting user table  (expecting success)
    def test_deleteTableEmptyU(self):
      createEmptyTables()
      err = tou.UserTable().deleteTable()
      errExp = pref.getError(pref.ERROR_SUCCESS)
      self.assertEqual(err,errExp)

    # Tests deleting script table (expecting success)
    def test_deleteTableEmptyS(self):
      createEmptyTables()
      err = tos.ScriptTable().deleteTable()
      errExp = pref.getError(pref.ERROR_SUCCESS)
      self.assertEqual(err,errExp)

    # Tests deleting computer table (expecting success)
    def test_deleteTableEmptyC(self):
      createEmptyTables()
      err = toc.ComputerTable().deleteTable()
      errExp = pref.getError(pref.ERROR_SUCCESS)
      self.assertEqual(err,errExp)

    # Tests deleting scriptLog table (expecting success)
    def test_deleteTableEmptySL(self):
      createEmptyTables()
      err = tosl.ScriptLogTable().deleteTable()
      errExp = pref.getError(pref.ERROR_SUCCESS)
      self.assertEqual(err,errExp)

    ################## DELETE NON-EMPTY TABLE TESTS (SUCCESS) ##################
    # Need to drop sql tables with foreign keys first i.e. order must be scriptLog, (computer, script), user. 
    # See details in https://sqlite.org/foreignkeys.html

    # Tests deleting user table containing records (expecting success)
    def test_deleteTableU_S(self):
      createTables()
      err = tosl.ScriptLogTable().deleteTable()
      err = tos.ScriptTable().deleteTable()
      err = toc.ComputerTable().deleteTable()
      err = tou.UserTable().deleteTable()
      errExp = pref.getError(pref.ERROR_SUCCESS)
      self.assertEqual(err,errExp)

    # Tests deleting script table containing records (expecting success)
    def test_deleteTableS_S(self):
      createTables()
      err = tosl.ScriptLogTable().deleteTable()
      err = tos.ScriptTable().deleteTable()
      errExp = pref.getError(pref.ERROR_SUCCESS)
      self.assertEqual(err,errExp)

    # Tests deleting computer table containing records (expecting success)
    def test_deleteTableC_S(self):
      createTables()
      err = tosl.ScriptLogTable().deleteTable()
      err = toc.ComputerTable().deleteTable()
      errExp = pref.getError(pref.ERROR_SUCCESS)
      self.assertEqual(err,errExp)

    # Tests deleting script log table containing records (expecting success)
    def test_deleteTableSL_S(self):
      createTables()
      err = tosl.ScriptLogTable().deleteTable()
      errExp = pref.getError(pref.ERROR_SUCCESS)
      self.assertEqual(err,errExp)

    ################## CREATE ENTRY (SUCCESS) ##################
    # Tests creating a script entry (expecting success).
    def test_createEntryS(self):
      createEmptyTables()
      s = tos.ScriptTable().createEntry("test_script_name", "test_script_name.sh", 0, "emptry script used for testing", False)
      self.assertEqual(s.name, "test_script_name")
      self.assertEqual(s.fileName, "test_script_name.sh")
      self.assertEqual(s.author, 0)
      self.assertEqual(s.desc, "emptry script used for testing")
      self.assertEqual(s.isAdmin, False)

    # Tests creating a computer entry (expecting success).
    def test_createEntryC(self):
      createEmptyTables()
      c = toc.ComputerTable().createEntry(0, "RachelsSurface", "Raquels Computer", "Rachel's wonderful awful computer", "rbroders", "idk how IPs are formatted ya yeet", False)
      self.assertEqual(c.userID, 0)
      self.assertEqual(c.name, "RachelsSurface")
      self.assertEqual(c.nickName, "Raquels Computer")
      self.assertEqual(c.desc, "Rachel's wonderful awful computer")
      self.assertEqual(c.username, "rbroders")
      self.assertEqual(c.IP, "idk how IPs are formatted ya yeet")
      self.assertEqual(c.asAdmin, False)

    # Tests creating a scriptLog entry (expecting success).
    def test_createEntrySL(self):
      createEmptyTables()
      sl = tosl.ScriptLogTable().createEntry(0, 0, 0, False)
      self.assertEqual(sl.scriptID, 0)
      self.assertEqual(sl.userID, 0)
      self.assertEqual(sl.compID, 0)
      self.assertEqual(sl.asAdmin, False)

    # Tests creating a user entry (expecting success).
    def test_createEntryU(self):
      createEmptyTables()
      u = tou.UserTable().createEntry("rbroders", "hella_secure_hashed_password", True)
      self.assertEqual(u.username, "rbroders")
      self.assertEqual(u.password, "hella_secure_hashed_password")
      self.assertEqual(u.admin, True)

    ################## ADD ENTRY (SUCCESS) ##################
    # Tests adding an entry to the user table. 
    # Must first create the entry then add it (expecting success).
    def test_addEntryU(self):
      createEmptyTables()
      u = tou.UserTable().createEntry("rbroders", "hella_secure_hashed_password", True)
      err = tou.UserTable().add(u)
      errExp = pref.getError(pref.ERROR_SUCCESS)
      self.assertEqual(err,errExp)
      self.assertEqual(u.ID, 1)

    # Tests adding an entry to the script table. 
    # Must first create the entry then add it (expecting success).
    # Due to foreign key constraints, entry in user table must first exist.
    def test_addEntryS(self):
      createEmptyTables()
      # need user entry first for foreign key
      u = tou.UserTable().createEntry("rbroders", "hella_secure_hashed_password", True)
      err = tou.UserTable().add(u) # uID will be 1
      # script entry
      s = tos.ScriptTable().createEntry("test_script_name", "test_script_name.sh", 1, "emptry script used for testing", False)
      err = tos.ScriptTable().add(s)
      errExp = pref.getError(pref.ERROR_SUCCESS)
      self.assertEqual(err,errExp)
      self.assertEqual(s.ID, 1)

    # Tests adding an entry to the computer table. 
    # Must first create the entry then add it (expecting success).
    # Due to foreign key constraints, entry in user table must first exist.
    def test_addEntryC(self):
      createEmptyTables()
      # need user entry first for foreign key
      u = tou.UserTable().createEntry("rbroders", "hella_secure_hashed_password", True)
      err = tou.UserTable().add(u) # uID will be 1
      # computer entry
      c = toc.ComputerTable().createEntry(1, "RachelsSurface", "Raquels Computer", "Rachel's wonderful awful computer", "rbroders", "idk how IPs are formatted ya yeet", False)
      err = toc.ComputerTable().add(c)
      errExp = pref.getError(pref.ERROR_SUCCESS)
      self.assertEqual(err,errExp)
      self.assertEqual(c.ID, 1)

    # Tests adding an entry to the scriptLog table. 
    # Must first create the entry then add it (expecting success).
    # Due to foreign key constraints, entry in user, script and computer tables must first exist.
    def test_addEntrySL(self):
      createEmptyTables()
      # need user entry first for foreign key
      u = tou.UserTable().createEntry("rbroders", "hella_secure_hashed_password", True)
      err = tou.UserTable().add(u) # uID will be 1
      # need script entry for foreign key
      s = tos.ScriptTable().createEntry("test_script_name", "test_script_name.sh", 1, "emptry script used for testing", False)
      err = tos.ScriptTable().add(s)
      # need computer entry for foreign key
      c = toc.ComputerTable().createEntry(1, "RachelsSurface", "Raquels Computer", "Rachel's wonderful awful computer", "rbroders", "idk how IPs are formatted ya yeet", False)
      err = toc.ComputerTable().add(c)
      # scriptLog entry
      sl = tosl.ScriptLogTable().createEntry(1, 1, 1, False)
      err = tosl.ScriptLogTable().add(sl)
      print(err)
      errExp = pref.getError(pref.ERROR_SUCCESS)
      # check stdout/stderr file creation
      outPath = pref.getNoCheck(pref.CONFIG_SCRIPT_LOG_PATH) + sl.stdoutFile
      errPath = pref.getNoCheck(pref.CONFIG_SCRIPT_LOG_PATH) + sl.stderrFile
      self.assertEqual(os.path.exists(outPath), True)
      self.assertEqual(os.path.exists(errPath), True)
      # check error and scriptlog ID
      self.assertEqual(err,errExp)
      self.assertEqual(sl.ID, 1)

    ################## DELETE NON-EMPTY TABLE TESTS (FAILURE) ##################
    # Tests deleting user table containing records (expecting failure)
    def test_deleteTableU_F(self):
      createTables()
      err = tou.UserTable().deleteTable()
      errExp = pref.getError(pref.ERROR_EXECUTE_SQLITE3_COMMAND, args = ("deleteTable", "User", "message")) 
      self.assertEqual(err,errExp)

    # Tests deleting script table containing records (expecting failure)
    def test_deleteTableS_F(self):
      createTables()
      err = tos.ScriptTable().deleteTable()
      errExp = pref.getError(pref.ERROR_EXECUTE_SQLITE3_COMMAND, args = ("deleteTable", "Script", "message")) 
      self.assertEqual(err,errExp)

    # Tests deleting computer table containing records (expecting failure)
    def test_deleteTableC_F(self):
      createTables()
      err = toc.ComputerTable().deleteTable()
      errExp = pref.getError(pref.ERROR_EXECUTE_SQLITE3_COMMAND, args = ("deleteTable", "Computer", "message")) 
      self.assertEqual(err,errExp)

    # Tests deleting script log table containing records (expecting success)
    # Note that test_deleteTableSL_F does not exist as the ScriptLog table's
    #     primary key is not referenced as a foreign key elsewhere

    ################## GETBYID TESTS (SUCCESS) ##################
    # Tests getByID for script. Confirms there are no errors and 
    #   that atributes of returned script are the same as entry 
    #   added in createTable helper function or expected in other way.
    def test_getByIDS(self):
      createTables()
      err, s = tos.ScriptTable().getByID(1)
      errExp = pref.getError(pref.ERROR_SUCCESS)
      self.assertEqual(err,errExp)
      self.assertEqual(s.ID, 1)
      self.assertEqual(s.name, "test_script_name")
      self.assertEqual(s.fileName, "test_script_name.sh")
      self.assertEqual(s.author, 1)
      self.assertEqual(s.desc, "empty script used for testing")
      self.assertEqual(s.size, 0.0)
      self.assertEqual(s.isAdmin, False)

    # Tests getByID for computer. Confirms there are no errors and 
    #   that atributes of returned computer are the same as entry 
    #   added in createTable helper function or expected in other way.
    def test_getByIDC(self):
      createTables()
      err, c = toc.ComputerTable().getByID(1)
      errExp = pref.getError(pref.ERROR_SUCCESS)
      self.assertEqual(err,errExp)
      self.assertEqual(c.ID, 1)
      self.assertEqual(c.userID, 1)
      self.assertEqual(c.name, "RachelsSurface")
      self.assertEqual(c.nickName, "Raquels Computer")
      self.assertEqual(c.desc, "Rachel's wonderful awful computer")
      self.assertEqual(c.username, "rbroders")
      self.assertEqual(c.IP, "idk how IPs are formatted ya yeet")
      self.assertEqual(c.asAdmin, False)

    # Tests getByID for scriptLog. Confirms there are no errors and 
    #   that atributes of returned scriptLog are the same as entry 
    #   added in createTable helper function or expected in other way.
    def test_getByIDSL(self):
      createTables()
      err, sl = tosl.ScriptLogTable().getByID(1)
      errExp = pref.getError(pref.ERROR_SUCCESS)
      self.assertEqual(err,errExp)
      self.assertEqual(sl.ID, 1)
      self.assertEqual(sl.scriptID, 1)
      self.assertEqual(sl.userID, 1)
      self.assertEqual(sl.compID, 1)
      self.assertEqual(sl.endTime, None)
      self.assertEqual(sl.returnVal, None)
      self.assertEqual(sl.errorCode, None)
      self.assertEqual(sl.stdoutFile, "STDOUT_test_script_name_1.log") # FIXME when getAttrByID implemented - "STDOUT_test_script_name_1.log"
      self.assertEqual(sl.stderrFile, "STDERR_test_script_name_1.log") # FIXME when getAttrByID implemented - "STDERR_test_script_name_1.log"
      self.assertEqual(sl.asAdmin, False)

    # Tests getByID for user. Confirms there are no errors and 
    #   that atributes of returned iser are the same as entry added 
    #   in createTable helper function or expected in other way.
    def test_getByIDU(self):
      createTables()
      err, u = tou.UserTable().getByID(1)
      errExp = pref.getError(pref.ERROR_SUCCESS)
      self.assertEqual(err,errExp)
      self.assertEqual(u.ID, 1)
      self.assertEqual(u.username, "rbroders")
      self.assertEqual(u.password, "hella_secure_hashed_password")
      self.assertEqual(u.admin, True)

    ################## GETATTRBYID TESTS (SUCCESS) ##################
    # These unit tests do not test all attributes for a given table but a select, representative few
    
    # Tests getAttrByID for script table (expecting success)
    def test_getAttrByIDS(self):
      # s = tos.ScriptTable().createEntry("test_script_name", "test_script_name.sh", 1, "empty script used for testing", False)
      createTables()
      errExp = pref.getError(pref.ERROR_SUCCESS)

      err, sID = tos.ScriptTable().getAttrByID("ID", 1)
      self.assertEqual(err,errExp)
      self.assertEqual(sID, 1)

      err, sName = tos.ScriptTable().getAttrByID("name", 1)
      self.assertEqual(err,errExp)
      self.assertEqual(sName, "test_script_name")

      err, sSize = tos.ScriptTable().getAttrByID("size", 1)
      self.assertEqual(err,errExp)
      self.assertEqual(sSize, 0.0)

      err, sAdmin = tos.ScriptTable().getAttrByID("isAdmin", 1)
      self.assertEqual(err,errExp)
      self.assertEqual(sAdmin, False)

    # Tests getAttrByID for computer table (expecting success)
    def test_getAttrByIDC(self):
      # c = toc.ComputerTable().createEntry(1, "RachelsSurface", "Raquels Computer", "Rachel's wonderful awful computer", "rbroders", "idk how IPs are formatted ya yeet", False)
      createTables()
      errExp = pref.getError(pref.ERROR_SUCCESS)

      err, cID = toc.ComputerTable().getAttrByID("ID", 1)
      self.assertEqual(err,errExp)
      self.assertEqual(cID, 1)

      err, cUserID = toc.ComputerTable().getAttrByID("userID", 1)
      self.assertEqual(err,errExp)
      self.assertEqual(cUserID, 1)

      err, cName = toc.ComputerTable().getAttrByID("name", 1)
      self.assertEqual(err,errExp)
      self.assertEqual(cName, "RachelsSurface")

      err, sUsername = toc.ComputerTable().getAttrByID("username", 1)
      self.assertEqual(err,errExp)
      self.assertEqual(sUsername, "rbroders")

      err, cAsAdmin = toc.ComputerTable().getAttrByID("asAdmin", 1)
      self.assertEqual(err,errExp)
      self.assertEqual(cAsAdmin, False)
    
    # Tests getAttrByID for scriptLog table (expecting success)
    def test_getAttrByIDSL(self):
      # sl = tosl.ScriptLogTable().createEntry(1, 1, 1, False)
      createTables()
      errExp = pref.getError(pref.ERROR_SUCCESS)

      err, slID = tosl.ScriptLogTable().getAttrByID("ID", 1)
      self.assertEqual(err,errExp)
      self.assertEqual(slID, 1)

      err, slCompID = tosl.ScriptLogTable().getAttrByID("compID", 1)
      self.assertEqual(err,errExp)
      self.assertEqual(slCompID, 1)

      err, slRetVal = tosl.ScriptLogTable().getAttrByID("returnVal", 1)
      self.assertEqual(err,errExp)
      self.assertEqual(slRetVal, None)

      err, slStdout = tosl.ScriptLogTable().getAttrByID("stdoutFile", 1)
      self.assertEqual(err,errExp)
      self.assertEqual(slStdout, "STDOUT_test_script_name_1.log")

      err, slAsAdmin = tosl.ScriptLogTable().getAttrByID("asAdmin", 1)
      self.assertEqual(err,errExp)
      self.assertEqual(slAsAdmin, False)

    # Tests getAttrByID for user table (expecting success)
    def test_getAttrByIDU(self):
      # u = tou.UserTable().createEntry("rbroders", "hella_secure_hashed_password", True)   
      errExp = pref.getError(pref.ERROR_SUCCESS)

      err, uID = tou.UserTable().getAttrByID("ID", 1)
      self.assertEqual(err,errExp)
      self.assertEqual(uID, 1)

      err, uUsername = tou.UserTable().getAttrByID("username", 1)
      self.assertEqual(err,errExp)
      self.assertEqual(uUsername, "rbroders")

      err, uPass = tou.UserTable().getAttrByID("password", 1)
      self.assertEqual(err,errExp)
      self.assertEqual(uPass, "hella_secure_hashed_password")

      err, uAdmin = tou.UserTable().getAttrByID("admin", 1)
      self.assertEqual(err,errExp)
      self.assertEqual(uAdmin, True)

    ################## GETALL TESTS (SUCCESS) ##################
    # These are pretty basic unit tests, could do more checks later

    # Tests getAll for script (expecting successs)
    def test_getAllS(self):
      createTablesBig()
      err, s = tos.ScriptTable().getAll()
      errExp = pref.getError(pref.ERROR_SUCCESS)
      self.assertEqual(err, errExp)

    # Tests getAll for computer (expecting successs)
    def test_getAllC(self):
      createTablesBig()
      err, c = toc.ComputerTable().getAll()
      errExp = pref.getError(pref.ERROR_SUCCESS)
      self.assertEqual(err, errExp)

    # Tests getAll for scriptLog (expecting successs)
    def test_getAllSL(self):
      createTablesBig()
      err, sl = tosl.ScriptLogTable().getAll()
      errExp = pref.getError(pref.ERROR_SUCCESS)
      self.assertEqual(err, errExp)

    # Tests getAll for user (expecting successs)
    def test_getAllU(self):
      createTablesBig()
      err, u = tou.UserTable().getAll()
      errExp = pref.getError(pref.ERROR_SUCCESS)
      self.assertEqual(err, errExp)

  
    # This function must stay at the bottom of the unit tests
    def cleanUp(self):
      resetConfig() # return to default database file


if __name__ == '__main__':
    unittest.main()
