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
                param = param + (value.strftime('%Y-%m-%d %H:%M:%S.%f'), )
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
        sl = None
        command = """SELECT * FROM sl WHERE ID = """ + str(ID) + """;"""
        e, slTuple = sqlFuncs.getRow(command, "getByID", "ScriptLog")
        # Also check error is pref.success
        if (e == pref.getError(pref.ERROR_SUCCESS)): 
            e, sl = tupleToScriptLog(slTuple, "getByID")
        return e, sl

    # overriding abstract method
    @staticmethod
    def getAll():
        '''
        Retreives all entries from the scriptLog SQL table and returns them as a list of scriptLog objects
        @param 
            None.
        @return 
            slList - list of scriptLog objects.
        '''
        command = """SELECT * FROM sl;"""
        e, rows = sqlFuncs.getAllRows(command, "getAll", "ScriptLog")
        slList = []
        if(e == pref.getError(pref.ERROR_SUCCESS)):
            for row in rows:
                e, sl = tupleToScriptLog(row, "getAll")
                if(e == pref.getError(pref.ERROR_SUCCESS)):
                    slList.append(sl)

        return e, slList

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
        return scriptLog 

    # overriding abstract method
    @staticmethod
    def getAttrByID(attr: str, ID: int):
        '''
        Retrieves a specified attrubute from an entry of the scriptLog SQL table based on primary key - ID
        @param 
            attr - one of the columns of the scriptLog table
            ID - primary key of scriptLog
        @return 
            e - error created during execution of function or Success if no error occurs
            s - the specified attribute's value from the entry retrieved from the SQL table 
        '''
        attr = None
        command = """SELECT (""" + attr + """) FROM sl WHERE ID = """ + str(ID) + """;"""
        e, slTuple = sqlFuncs.getRow(command, "getAttrByID", "ScriptLog")
        if(e == pref.getError(pref.ERROR_SUCCESS)):
            attr = slTuple[0]
        return e, attr

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
        ID = None
        command = """ INSERT INTO sl (id, scriptID, userID, compID, startTime, endTime, returnVal, errorCode, stdoutFile, stderrFile, asAdmin) VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
        data = entry.paramToList()
        e, ID = sqlFuncs.insert(command, data, "add", "ScriptLog")
        entry.ID = ID # access ID through entry object after executing this function
        ######### create names/files for stdoutFile, stderrFile - {STDOUT/STDERR}_SCRIPT_ID.log #########
        # (1) Add names to entry object
        if(e == pref.getError(pref.ERROR_SUCCESS)):
            e, scriptName = tos.ScriptTable().getAttrByID("name", entry.scriptID)
            if e == pref.getError(pref.ERROR_SUCCESS):
                entry.stdoutFile = "STDOUT_" + str(scriptName) + "_" + str(ID) + ".log"  # access stdoutFile through entry object after executing this function
                entry.stderrFile = "STDERR_" + str(scriptName) + "_" + str(ID) + ".log"  # access stderrFile through entry object after executing this function
                # (2) Write names to sql entry
                command2 = """UPDATE sl SET stdoutFile = \"""" + str(entry.stdoutFile) + """\", stderrFile = \"""" + str(entry.stderrFile) + """\" WHERE id = """ + str(ID) + """;"""
                e = sqlFuncs.exeCommand(command2, "add", "ScriptLog")
                # (3) Create files 
                e = createFile(e, pref.getNoCheck(pref.CONFIG_SCRIPT_LOG_PATH), entry.stdoutFile)
                e = createFile(e, pref.getNoCheck(pref.CONFIG_SCRIPT_LOG_PATH), entry.stderrFile)
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
    def editEntry(entry: ScriptLog):
        '''
        Updates a row in the scriptLog SQL table based on the entry object passed. 
        Overwrites all attributes of the row with the values of the entry object.
        Overwrites row based on the ID of the entry object.
        @param 
            entry: ScriptLog - ScriptLog object, must have ID != None or error will be thrown
        @return 
            e - most recent error when executing function or Success if no error occurs
            sl - ScriptLog object corresponding to row updated in SQL table. Should be the 
                same as entry passed to function if no error occured
        '''
        sl = entry

        if(entry.ID == None):
            e = pref.getError(pref.ERROR_NO_ID_PROVIDED, args=("editEntry", "ScriptLog"))

        else:
            command = """UPDATE sl SET """
            for attr, value in entry.__dict__.items():
                if (attr == "ID"):
                    pass
                else:
                    command = command + str(attr)
                    if(value == None):
                        command = command + """ = NULL"""
                    elif attr[-4:] == "Time":
                        command = command + """ = """ + """\"""" + str(value.strftime('%Y-%m-%d %H:%M:%S.%f')) + """\""""
                    elif isinstance(value, str):
                        command = command + """ = """ + """\"""" + str(value) + """\""""
                    else:
                        command = command + """ = """ + str(value)
                    command = command + """, """
            command = command[:-2] #remove last ' ,'
            command = command + """ WHERE ID = """ + str(entry.ID) + """;"""
            print(command)

            e = sqlFuncs.exeCommand(command, "editEntry", "ScriptLog")

            if(e == pref.getError(pref.ERROR_SUCCESS)):
                command2 = """SELECT * FROM sl WHERE ID = """ + str(entry.ID) + """;"""
                e, row = sqlFuncs.getRow(command2, "editEntry", "ScriptLog")
                if(e == pref.getError(pref.ERROR_SUCCESS)):
                    e, sl = tupleToScriptLog(row, "editEntry")

        return e, sl


def createFile(e, path, filename):
    '''
    Creates a file of name 'filename' located at 'path'. Updates error 'e' with any errors that occur throughout this function.
    @param 
        e - current error from where createFile is called
        path - location of file to be created
        filename - name of file to be created
    @return 
        e - updated error
    '''
    try:
        f = open(path + filename, "w")
    except OSError as osE:
        print("osE: ")
        print(osE)
        print("filename: " + filename)
        e = pref.getError(pref.ERROR_CANT_CREATE_FILE, args = (filename))
    return e

def tupleToScriptLog(tup: tuple, commandName: str):
    '''
    Seperates a tuple of scriptLog object parameter values to init a scriptLog object
    @param 
        tup - a tuple containing values for every parameter of the scriptLog class
    @return 
        scriptLog object
    '''
    # ID: int, scriptID: int, userID: int, compID: int, startTime: datetime.datetime,
    # endTime: datetime.datetime, returnVal: int, errorCode: int, stdoutFile: str, stderrFile: str,
    # asAdmin: bool 
    e = pref.getError(pref.ERROR_SUCCESS)
    if(len(tup) != 11):
        e = pref.getError(pref.ERROR_SQL_RETURN_MISSING_ATTR, args=(commandName, "ScriptLog", len(tup), 11))
        sl = None
    else:
        try:
            if(tup[0] == None):
                ID = None
            else:
                ID = int(tup[0])

            if(tup[1] == None):
                scriptID = None
            else:
                scriptID = int(tup[1])

            if(tup[2] == None):
                userID = None
            else:
                userID = int(tup[2])

            if(tup[3] == None):
                compID = None
            else:
                compID = int(tup[3])

            if(tup[4] == None):
                startTime = None
            else:
                startTime = datetime.datetime.strptime(tup[4], '%Y-%m-%d %H:%M:%S.%f')

            if(tup[5] == None):
                endTime = None
            else:
                endTime = datetime.datetime.strptime(tup[5], '%Y-%m-%d %H:%M:%S.%f')

            if(tup[6] == None):
                returnVal = None
            else:
                returnVal = int(tup[6])

            if(tup[7] == None):
                errorCode = None
            else:
                errorCode = int(tup[7])

            if(tup[8] == None):
                stdoutFile = None
            else:
                stdoutFile = str(tup[8])

            if(tup[9] == None):
                stderrFile = None
            else:
                stderrFile = str(tup[9])

            if(tup[10] == None):
                asAdmin = None
            else:
                asAdmin = bool(tup[10])

            sl = ScriptLog(ID, scriptID, userID, compID, startTime, endTime, returnVal, errorCode, stdoutFile, stderrFile, asAdmin)
        except ValueError as err:
            e = pref.getError(pref.ERROR_SQL_RETURN_CAST, args=(commandName, "ScriptLog", err))
            sl = None

    return e, sl