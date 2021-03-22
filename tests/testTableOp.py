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

class BaseTestCase(unittest.TestCase):
    # Tests table creation from user class directly
    def test_createTableU(self):
      err = tou.UserTable().createTable()
      self.assertEqual(err,pref.getError(pref.ERROR_SUCCESS))

    # Tests table creation from script class directly
    def test_createTableS(self):
      err = tos.ScriptTable().createTable()
      self.assertEqual(err,pref.getError(pref.ERROR_SUCCESS))

    # Tests table creation from computer class directly
    def test_createTableC(self):
      err = toc.ComputerTable().createTable()
      self.assertEqual(err,pref.getError(pref.ERROR_SUCCESS))

    # Tests table creation from scriptLog class directly
    def test_createTableSL(self):
      err = tosl.ScriptLogTable().createTable()
      self.assertEqual(err,pref.getError(pref.ERROR_SUCCESS))



    
      



if __name__ == '__main__':
    unittest.main()


# testScript = tos.Script(1, "SkeletonScriptName1", "SkeletonScriptName1.py", 1, "Skeleton Script Description 1",datetime.datetime.now(), datetime.datetime.now(), 0, False)
# testScriptLog = tosl.ScriptLog(0, 0, 0, 0, datetime.datetime.now(), datetime.datetime.now(), 1, 1, "stdoutFile.txt", "stderrFile.txt", False)
# testComputer = toc.Computer(0, 0, "RachelsComputer", "RaquelsComp", "Rachel's computer description", "some IP address idk", datetime.datetime.now(), datetime.datetime.now(), False)
# testUser = tou.User(0, "username1", "hashed password 1", datetime.datetime.now(), datetime.datetime.now(), False)

# testTupleS = (1, "SkeletonScriptName1", "SkeletonScriptName1.py", 1, "Skeleton Script Description 1",datetime.datetime.now(), datetime.datetime.now(), 0, False)
# testTupleSL = (0, 0, 0, 0, datetime.datetime.now(), datetime.datetime.now(), 1, 1, "stdoutFile.txt", "stderrFile.txt", False)
# testTupleC = (0, 0, "RachelsComputer", "RaquelsComp", "Rachel's computer description", "some IP address idk", datetime.datetime.now(), datetime.datetime.now(), False)
# testTupleU = (0, "username1", "hashed password 1", datetime.datetime.now(), datetime.datetime.now(), False)

# testScript.toJson()
# testScriptLog.toJson()
# testComputer.toJson()
# testUser.toJson()

# testScriptTable = tos.ScriptTable()
# testScriptLogTable = tosl.ScriptLogTable()
# testComputerTable = toc.ComputerTable()
# testUserTable = tou.UserTable()

# testScriptTable.createTable()
# testScriptTable.getByID(0)
# testScriptTable.getAll()
# testScriptTable.createEntry(testTupleS)
# testScriptTable.getAttrByID("ID", 0)
# testScriptTable.getWithQuery("")
# testScriptTable.add(testScript)
# testScriptTable.delete(0)
# testScriptTable.editEntry(testTupleS)

# testScriptLogTable.createTable()
# testScriptLogTable.getByID(0)
# testScriptLogTable.getAll()
# testScriptLogTable.createEntry(testTupleSL)
# testScriptLogTable.getAttrByID("ID", 0)
# testScriptLogTable.getWithQuery("")
# testScriptLogTable.add(testScriptLog)
# testScriptLogTable.delete(0)
# testScriptLogTable.editEntry(testTupleSL)

# testComputerTable.createTable()
# testComputerTable.getByID(0)
# testComputerTable.getAll()
# testComputerTable.createEntry(testTupleC)
# testComputerTable.getAttrByID("ID", 0)
# testComputerTable.getWithQuery("")
# testComputerTable.add(testComputer)
# testComputerTable.delete(0)
# testComputerTable.editEntry(testComputer)

# testUserTable.createTable()
# testUserTable.getByID(0)
# testUserTable.getAll()
# testUserTable.createEntry(testTupleU)
# testUserTable.getAttrByID("ID", 0)
# testUserTable.getWithQuery("")
# testUserTable.add(testUser)
# testUserTable.delete(0)
# testUserTable.editEntry(testUser)