import datetime
from datetime import datetime as dt
import libpurpl3.preferences as pref
import libpurpl3.tableOp as tableOp
import libpurpl3.sqlFuncs as sqlFuncs
import libpurpl3.tableOpScript as tos
import sqlite3

class ScriptLog(tableOp.Entry):
    # TODO add default values
    # overriding abstract method
    def __init__(self, ID: int, scriptID: int, userID: int, compID: int, startTime: datetime.datetime,
                endTime: datetime.datetime, returnVal: int, errorCode: int, stdoutFile: str, stderrFile: str,
                 asAdmin: bool):
        '''
        Creates scriptLog object. Contains all info on the execution of a given script on a given computer by a specific user.
        @param 
            ID: int - unique identifier automatically generated when scriptLog is added to sql table. Will be None until scriptLog is added to table.
            scriptID: int - primary key of script table to indicate which script was executed
            userID: int - primary key of user table to indicate which user executed script
            compID: int - primary key of computer table to indictae which computer is having script executed on it
            startTime: datetime.datetime - dateTime when createEntry is called for the scriptLog
            endTime: datetime.datetime - dateTime when createEntry script execution is finished
            returnVal: int - value returned from script execution 
            errorCode: int - error code returned from script execution
            stdoutFile: str - file location where stdout logs will be stored from script execution
            stderrFile: str - file location where stderr logs will be stored from script execution
            asAdmin: bool - whether or not the script was executed as admin
        @return 
            None.
        '''
        self.ID = ID
        self.scriptID = scriptID
        self.userID = userID
        self.compID = compID
        self.startTime = startTime
        self.endTime = endTime
        self.returnVal = returnVal
        self.errorCode = errorCode
        self.stdoutFile = stdoutFile
        self.stderrFile = stderrFile
        self.asAdmin = asAdmin

    # overriding abstract method
    def toJson(self):
        '''
        Returns a dictionary of all object attributes as strings.
        @param 
            None.
        @return
            Dictionary of all object attributes as strings.
        '''
        return {
            "ID": str(self.ID),
            "scriptID": str(self.scriptID),
            "userID": str(self.userID),
            "compID": str(self.compID),
            "startTime": str(self.startTime),
            "endTime": str(self.endTime),
            "returnVal": str(self.returnVal),
            "errorCode": str(self.errorCode),
            "stdoutFile": str(self.stdoutFile),
            "stderrFile": str(self.stderrFile),
            "asAdmin": str(self.asAdmin)
        }

    def paramToList(self):
        '''
        Returns all the parameters of a scriptLog object as a tuple that can be used for SQL calls.
        Omits id from tuple as id will be automatically generated using AUTOINCREMENT when the script object is added to the table.
        @param 
            None.
        @return 
            param - tuple of all attribute's values for scriptLog object, omitting ID
        '''
        param = ()
        for attr, value in self.__dict__.items():
            if attr == "ID":
                pass
            elif attr[0:2] == "dt":
                param = param + (value.strftime('%Y-%m-%d %H:%M:%S'), )
            else:
                param = param + (value, )
        return param


class ScriptLogTable(tableOp.Table):
    # overriding abstract method
    @staticmethod
    def createTable():
        '''
        creates an empty SQL table for scripts
        @param None.
        @return errorCode: Error
        '''
        command = """CREATE TABLE IF NOT EXISTS sl (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       scriptId INTEGER,
                       userId INTEGER,
                       compId INTEGER,
                       startTime DATETIME,
                       endTime DATETIME,
                       returnVal INTEGER,
                       errorCode INTEGER,
                       stdoutFile CHAR(256),
                       stderrFile CHAR(256),
                       asAdmin BOOL,
                       FOREIGN KEY (scriptId) REFERENCES s(id),
                       FOREIGN KEY (userId) REFERENCES u(id),
                       FOREIGN KEY (compId) REFERENCES c(id)
                    );"""
        # e = sqlFuncs.createTable(command, "ScriptLog")
        e = sqlFuncs.exeCommand(command, "createTable", "ScriptLog")
        return e

    # overriding abstract method
    @staticmethod
    def deleteTable():
        '''
        Removes the scriptLog SQL table from the database. Used for testing principally.
        @param None.
        @return e - Error code, returns success if no error occurs.
        '''
        command = """DROP TABLE sl;
                  """
        e = sqlFuncs.exeCommand(command, "deleteTable", "ScriptLog")
        return e

    # overriding abstract method
    @staticmethod
    def getByID(ID: int):
        '''
        Retrieves an entry from the scriptLog SQL table based on primary key - ID
        @param 
            ID - primary key of scriptLog
        @return 
            e - error created during execution of function or Success if no error occurs
            s - the entry retrieved from the SQL table as a ScriptLog object
        '''
        command = """SELECT * FROM sl WHERE ID = """ + str(ID) + """;"""
        e, slTuple = sqlFuncs.getRow(command, "getByID", "ScriptLog")
        sl = ScriptLog(slTuple[0], slTuple[1], slTuple[2], slTuple[3], slTuple[4], slTuple[5], slTuple[6], slTuple[7], slTuple[8], slTuple[9], slTuple[10])
        return e, sl

    # overriding abstract method
    @staticmethod
    def getAll():
        '''
        #TODO
        *add description*.
        @param *add param*.
        @return *add return*.
        '''
        skelScriptLog1 = ScriptLog(0, 0, 0, 0, datetime.datetime.now(), datetime.datetime.now(), 1, 1,
                                   "stdoutFile1.txt", "stderrFile1.txt", False)
        skelScriptLog2 = ScriptLog(1, 0, 0, 0, datetime.datetime.now(), datetime.datetime.now(), 1, 1,
                                   "stdoutFile2.txt", "stderrFile2.txt", False)
        scriptLogs = (skelScriptLog1, skelScriptLog2)
        return pref.getError(pref.ERROR_SUCCESS), scriptLogs

    # overriding abstract method
    @staticmethod
    def createEntry(scriptID: int, userID: int, compID: int, asAdmin: bool):
        '''
        Creates a scriptLog object. Some parameters must be passed in, some will be calculated 
        in this function and some can only be filled when the scriptLog is added to the SQL 
        table (these parameters will be set to None until the scriptLog is added to the SQL table).
        @param 
            scriptID: int - primary key of script table to indicate which script was executed
            userID: int - primary key of user table to indicate which user executed script
            compID: int - primary key of computer table to indictae which computer is having script executed on it
            asAdmin: bool - whether or not the script was executed as admin
        @return 
            Error - error object indicating if any error was encountered when creating the script object 
            scriptLog - scriptLog object created
        '''
        # id will be set when object is added to table
        id = None
        # set startTime to "now"
        startTime = dt.now()
        # endTime, returnVal, errorCode are none - will be created through calls to editEntry
        endTime = None
        returnVal = None
        errorCode = None
        # create names/files for stdoutFile, stderrFile - {STDOUT/STDERR}_SCRIPT_ID.log requires scriptLog ID and thus must be done in add function
        stdoutFile = None
        stderrFile = None
        # create scriptLog object
        scriptLog = ScriptLog(id, scriptID, userID, compID, startTime, endTime, returnVal, errorCode, stdoutFile, stderrFile, asAdmin)
        return pref.getError(pref.ERROR_SUCCESS), scriptLog #FIXME - error is redundant, take out???

    # overriding abstract method
    @staticmethod
    def getAttrByID(attr: str, ID: int):
        '''
        #TODO
        *add description*.
        @param *add param*.
        @return *add return*.
        '''
        # int
        if (attr == "ID" or attr == "scriptID" or attr == "userID" or attr == "compID" or attr == "returnVal" or
                attr == "errorCode"):
            return pref.getError(pref.ERROR_SUCCESS), 0
        # str
        elif (attr == "stdoutFile" or attr == "stderrFile"):
            return pref.getError(pref.ERROR_SUCCESS), ""
        # datetime
        elif (attr == "startTime" or attr == "endTime"):
            return pref.getError(pref.ERROR_SUCCESS), datetime.datetime.now()
        # bool
        elif (attr == "asAdmin"):
            return pref.getError(pref.ERROR_SUCCESS), False
        else:
            return pref.getError(pref.ERROR_ATTRIBUTE_NOT_FOUND), None

    # overriding abstract method
    @staticmethod
    def getWithQuery(query: str):
        '''
        #TODO
        *add description*.
        @param *add param*.
        @return *add return*.
        '''
        skelScriptLog = ScriptLog(0, 0, 0, 0, datetime.datetime.now(), datetime.datetime.now(), 1, 1, "stdoutFile1.txt",
                               "stderrFile1.txt", False)
        return pref.getError(pref.ERROR_SUCCESS), skelScriptLog

    # overriding abstract method
    @staticmethod
    def add(entry: ScriptLog):
        '''
        Takes a scriptLog object (which has not yet been added to the scriptLog SQL table), 
            adds it to the table and updates scriptLog object's ID (ID is automatically 
            generated using sqlite AUTOINCREMENT) 
        This function is meant to take a scriptLog object generated from a call to the 
            createEntry function.
        @param 
            entry - object of class ScriptLog
        @return 
            e - most recent error when executing function or Success if no error occurs
        '''
        ID = 0
        command = """ INSERT INTO sl (id, scriptID, userID, compID, startTime, endTime, returnVal, errorCode, stdoutFile, stderrFile, asAdmin) VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
        data = entry.paramToList()
        e, ID = sqlFuncs.insert(command, data, "add", "ScriptLog")
        entry.ID = ID # access ID through entry object after executing this function
        ######### create names/files for stdoutFile, stderrFile - {STDOUT/STDERR}_SCRIPT_ID.log #########
        # (1) Add names to entry object
        e, scriptName = tos.ScriptTable().getAttrByID("name", entry.scriptID)
        if e == pref.getError(pref.ERROR_SUCCESS):
            entry.stdoutFile = "STDOUT_" + str(scriptName) + "_" + str(ID) + ".log"  # access stdoutFile through entry object after executing this function
            entry.stderrFile = "STDERR_" + str(scriptName) + "_" + str(ID) + ".log"  # access stderrFile through entry object after executing this function
            # (2) Write names to sql entry
            command2 = """UPDATE sl SET stdoutFile = \"""" + str(entry.stdoutFile) + """\", stderrFile = \"""" + str(entry.stderrFile) + """\" WHERE id = """ + str(ID) + """;"""
            e = sqlFuncs.exeCommand(command2, "add", "ScriptLog")
            # (3) Create files 
            e = createFile(e, pref.getNoCheck("SCRIPT_LOG_PATH"), entry.stdoutFile)
            e = createFile(e, pref.getNoCheck("SCRIPT_LOG_PATH"), entry.stderrFile)
        return e #FIXME - should actions be undone if any errors occur along the way *thinking* - for loop

    # overriding abstract method
    @staticmethod
    def delete(ID: int):
        '''
        #TODO
        *add description*.
        @param *add param*.
        @return *add return*.
        '''
        return pref.getError(pref.ERROR_SUCCESS)

    # overriding abstract method
    @staticmethod
    def editEntry(values: tuple):
        '''
        #TODO
        *add description*.
        @param *add param*.
        @return *add return*.
        '''
        skelScriptLog = ScriptLog(0, 0, 0, 0, datetime.datetime.now(), datetime.datetime.now(), 1, 1, "stdoutFile1.txt",
                                  "stderrFile1.txt", False)
        return pref.getError(pref.ERROR_SUCCESS), skelScriptLog


def createFile(e, path, filename):
    try:
        f = open(path + filename, "w")
    except OSError as osE:
        print("osE: ")
        print(osE)
        print("filename: " + filename)
        e = pref.getError(pref.ERROR_CANT_CREATE_FILE, args = (filename))
    return e
