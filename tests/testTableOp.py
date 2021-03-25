import libpurpl3.tableOp as to
import libpurpl3.tableOpScript as tos
import libpurpl3.tableOpScriptLog as tosl
import libpurpl3.tableOpComputer as toc
import libpurpl3.tableOpUser as tou
import libpurpl3.preferences as pref
import libpurpl3.sqlFuncs as sqlFuncs
import sqlite3
import datetime
import unittest

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
    Create tables (scriptLog, script, computer and user) with some records inserted into each of them
    @param None.
    @return None.
    '''
    createEmptyTables()
    # TODO insert records

class BaseTestCase(unittest.TestCase):
    def setUp(self):
      pref.setAttr("DB_PATH", "unit_test.db") # work on seperate clean database so as to not mess up test data in base db

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
    def test_createEntryS(self):
      createTables()
      err, s = tos.ScriptTable().createEntry("test_script_name", "test_script_name.sh", 0, "emptry script used for testing", False)
      errExp = pref.getError(pref.ERROR_SUCCESS)
      self.assertEqual(err,errExp)
      self.assertEqual(s.name, "test_script_name")
      self.assertEqual(s.fileName, "test_script_name.sh")
      self.assertEqual(s.author, 0)
      self.assertEqual(s.desc, "emptry script used for testing")
      self.assertEqual(s.isAdmin, False)

    def test_createEntryC(self):
      createTables()
      err, c = toc.ComputerTable().createEntry(0, "RachelsSurface", "Raquels Computer", "Rachel's wonderful awful computer", "rbroders", "idk how IPs are formatted ya yeet", False)
      errExp = pref.getError(pref.ERROR_SUCCESS)
      self.assertEqual(err,errExp)
      self.assertEqual(c.userID, 0)
      self.assertEqual(c.name, "RachelsSurface")
      self.assertEqual(c.nickName, "Raquels Computer")
      self.assertEqual(c.desc, "Rachel's wonderful awful computer")
      self.assertEqual(c.username, "rbroders")
      self.assertEqual(c.IP, "idk how IPs are formatted ya yeet")
      self.assertEqual(c.asAdmin, False)

    def test_createEntrySL(self):
      createTables()
      err, sl = tosl.ScriptLogTable().createEntry(0, 0, 0, False)
      errExp = pref.getError(pref.ERROR_SUCCESS)
      self.assertEqual(err,errExp)
      self.assertEqual(sl.scriptID, 0)
      self.assertEqual(sl.userID, 0)
      self.assertEqual(sl.compID, 0)
      self.assertEqual(sl.asAdmin, False)

    def test_createEntryU(self):
      createTables()
      err, u = tou.UserTable().createEntry("rbroders", "hella_secure_hashed_password", True)
      errExp = pref.getError(pref.ERROR_SUCCESS)
      self.assertEqual(err,errExp)
      self.assertEqual(u.username, "rbroders")
      self.assertEqual(u.password, "hella_secure_hashed_password")
      self.assertEqual(u.admin, True)



  


    # TODO - these tests will fail until createTables is correctly implemented
    ################## DELETE NON-EMPTY TABLE TESTS (FAILURE) ##################
    # # Tests deleting user table containing records (expecting failure)
    # def test_deleteTableU_F(self):
    #   createTables()
    #   err = tou.UserTable().deleteTable()
    #   errExp = pref.getError(pref.ERROR_EXECUTE_SQLITE3_COMMAND, args = ("deleteTable", "User", "message")) #TODO find out what message would be
    #   self.assertEqual(err,errExp)

    # # Tests deleting script table containing records (expecting failure)
    # def test_deleteTableS_F(self):
    #   createTables()
    #   err = tos.ScriptTable().deleteTable()
    #   errExp = pref.getError(pref.ERROR_EXECUTE_SQLITE3_COMMAND, args = ("deleteTable", "Script", "message")) #TODO find out what message would be
    #   self.assertEqual(err,errExp)

    # # Tests deleting computer table containing records (expecting failure)
    # def test_deleteTableC_F(self):
    #   createTables()
    #   err = toc.ComputerTable().deleteTable()
    #   errExp = pref.getError(pref.ERROR_EXECUTE_SQLITE3_COMMAND, args = ("deleteTable", "Computer", "message")) #TODO find out what message would be
    #   self.assertEqual(err,errExp)

    # Tests deleting script log table containing records (expecting success)
    # Note that test_deleteTableSL_F does not exist as the ScriptLog table's
    #     primary key is not referenced as a foreign key elsewhere


    # This function must stay at the bottom of the unit tests
    def cleanUp(self):
      resetConfig() # return to default database file


if __name__ == '__main__':
    unittest.main()
