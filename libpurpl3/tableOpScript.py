import datetime
from datetime import datetime as dt
import libpurpl3.preferences as pref 
import libpurpl3.tableOp as tableOp
import libpurpl3.sqlFuncs as sqlFuncs
import sqlite3
import os

class Script(tableOp.Entry):
    # overriding abstract method
    def __init__(self, ID: int, name: str, fileName: str, author: int, desc: str, dtCreated: datetime.datetime,
                 dtModified: datetime.datetime, size: float, isAdmin: bool):
        '''
        Creates a script object with all info on a script.
        @param 
            ID: int - unique identifier automatically generated when script is added to sql table. Will be None until script is added to table.
            name: str - use defined name to identify file 
            fileName: str - identifying fileName
            author: int - primary key of user table to indicate which user created the script 
            desc: str - user defined script description
            dtCreated: datetime.datetime - dateTime when createEntry is called for the script
            dtModified: datetime.datetime - dateTime when createEntry is called for the script or when editEntry is called
            size: float - size of file containing script (in bytes)
            isAdmin: bool - whether or not the script requires admin access to run
        @return 
            None
        '''
        self.ID = ID
        self.name = name
        self.fileName = fileName
        self.author = author
        self.desc = desc
        self.dtCreated = dtCreated
        self.dtModified = dtModified
        self.size = size
        self.isAdmin = isAdmin

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
            "name": str(self.name),
            "fileName": str(self.fileName),
            "author": str(self.author),
            "desc": str(self.desc),
            "dtCreated": str(self.dtCreated),
            "dtModified": str(self.dtModified),
            "size": str(self.size),
            "isAdmin": str(self.isAdmin)
        }

    def paramToList(self):
        '''
        Returns all the parameters of a script object as a tuple that can be used for SQL calls.
        Omits id from tuple as id will be automatically generated using AUTOINCREMENT when the script object is added to the table.
        @param 
            None.
        @return 
            param - tuple of all attribute's values for script object, omitting ID
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



class ScriptTable(tableOp.Table):
    # overriding abstract method
    @staticmethod
    def createTable():
        '''
        creates an empty SQL table for scripts
        @param None.
        @return errorCode: Error
        '''
        command = """CREATE TABLE IF NOT EXISTS s (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       name CHAR(256),
                       fileName CHAR(256),
                       author INTEGER,
                       desc CHAR(1024),
                       dtCreated DATETIME,
                       dtModified DATETIME,
                       size FLOAT(5, 3),
                       isAdmin BOOL,
                       FOREIGN KEY (author)
                        REFERENCES u(id)
                        ON DELETE CASCADE
                    );"""
        e = sqlFuncs.exeCommand(command, "createTable", "Script")
        return e

    # overriding abstract method
    @staticmethod
    def deleteTable():
        '''
        Removes the script SQL table from the database. Used for testing principally.
        @param None.
        @return e - Error code, returns success if no error occurs.
        '''
        command = """DROP TABLE s;
                  """
        e = sqlFuncs.exeCommand(command, "deleteTable", "Script")
        return e

    # overriding abstract method
    @staticmethod 
    def getByID(ID: int):
        '''
        Retrieves an entry from the script SQL table based on primary key - ID
        @param 
            ID - primary key of script
        @return 
            e - error created during execution of function or Success if no error occurs
            s - the entry retrieved from the SQL table as a Script object
        '''
        command = """SELECT * FROM s WHERE ID = """ + str(ID) + """;"""
        s = None
        e, scriptTuple = sqlFuncs.getRow(command, "getByID", "Script") 
        if(e == pref.getError(pref.ERROR_SUCCESS)):
            e, s = tupleToScript(scriptTuple, "getByID")
        return e, s

    # overriding abstract method
    @staticmethod
    def getAll():
        '''
        Retreives all entries from the script SQL table and returns them as a list of script objects
        @param 
            None.
        @return 
            sList - list of script objects.
        '''
        command = """SELECT * FROM s;"""
        e, rows = sqlFuncs.getAllRows(command, "getAll", "Script")
        sList = []
        if(e == pref.getError(pref.ERROR_SUCCESS)):
            if (rows != None):
                for row in rows:
                    e, s = tupleToScript(row, "getAll")
                    if(e == pref.getError(pref.ERROR_SUCCESS)):
                        sList.append(s)

        return e, sList

    # overriding abstract method
    @staticmethod
    def createEntry(name: str, fileName: str, author: int, desc: str, isAdmin: bool): 
        '''
        Creates a script object. Some parameters must be passed in, some will be calculated 
        in this function and some can only be filled when the script is added to the SQL 
        table (these parameters will be set to None until the script is added to the SQL table).
        @param 
            name: str - use defined name to identify file 
            fileName: str - identifying fileName
            author: int - primary key of user table to indicate which user created the script 
            desc: str - user defined script description
            isAdmin: bool - whether or not the script requires admin access to run
        @return 
            script - script object created
        '''
        script = None
        # id will be set when object is added to table
        id = None
        # set dtCreated
        dtCreated = dt.now()
        # set dtModified (will be same as dtCreated initially)
        dtModified = dtCreated
        # set size
        filePath = str(pref.getNoCheck(pref.CONFIG_SCRIPT_PATH)) + fileName
        try:
            fileStats = os.stat(filePath)
            fileSizeB = fileStats.st_size
        except OSError as err:
            fileSizeB = 0.0 # set size to zero script file does not exist

        # create script object
        script = Script(None, name, fileName, author, desc, dtCreated, dtModified, fileSizeB, isAdmin)

        return script 

    # overriding abstract method
    @staticmethod
    def getAttrByID(attr: str, ID: int):
        '''
        Retrieves a specified attrubute from an entry of the script SQL table based on primary key - ID
        @param 
            attr - one of the columns of the script table
            ID - primary key of script
        @return 
            e - error created during execution of function or Success if no error occurs
            s - the specified attribute's value from the entry retrieved from the SQL table 
        '''
        val = None
        command = """SELECT (""" + attr + """) FROM s WHERE ID = """ + str(ID) + """;"""
        e, sTuple = sqlFuncs.getRow(command, "getAttrByID", "Script")
        if(e == pref.getError(pref.ERROR_SUCCESS)):
            if(sTuple == None):
                e = pref.getError(pref.ERROR_SQL_RETURN_MISSING_ATTR, args=("getAttrByID", "Script", 0, 1))
            elif(len(sTuple) != 1):
                e = pref.getError(pref.ERROR_SQL_RETURN_MISSING_ATTR, args=("getAttrByID", "Script", len(sTuple), 1))
            else:
                val = sTuple[0]
        return e, val

    # overriding abstract method
    @staticmethod
    def getWithQuery(query: str):
        '''
        #TODO
        *add description*.
        @param *add param*.
        @return *add return*.
        '''
        skelScript = Script(0, "SkeletonScriptName", "SkeletonScriptName.py", 1, "Skeleton Script Description", datetime.datetime.now(), datetime.datetime.now(), 0, False)
        return pref.getError(pref.ERROR_SUCCESS), skelScript

    # overriding abstract method
    @staticmethod
    def add(entry: Script): 
        '''
        Takes a script object (which has not yet been added to the script SQL table), 
            adds it to the table and updates script object's ID (ID is automatically 
            generated using sqlite AUTOINCREMENT) 
        This function is meant to take a script object generated from a call to the 
            createEntry function.
        @param 
            entry - object of class Script
        @return 
            e - most recent error when executing function or Success if no error occurs
        '''
        ID = None
        command = """ INSERT INTO s (id, name, fileName, author, desc, dtCreated, dtModified, size, isAdmin) VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?)"""
        data = entry.paramToList()
        e, ID = sqlFuncs.insert(command, data, "add", "Script")
        entry.ID = ID # access ID through entry object after executing this function
        return e

    # overriding abstract method
    @staticmethod
    def delete(ID: int):
        '''
        Removes a script entry from the database based on it's ID. 
        Also removes the corresponding file from directory.
        @param 
            ID: int - primary key of script
        @return 
            e - most recent error when executing function or Success if no error occurs
        '''
        e, fileName = ScriptTable.getAttrByID("fileName", ID)
        if(e == pref.getError(pref.ERROR_SUCCESS)):
            command = """DELETE FROM s WHERE ID = """ + str(ID) + """;"""
            e = sqlFuncs.exeCommand(command, "delete", "Script")
            if(e == pref.getError(pref.ERROR_SUCCESS)): # If deleted from db successfully, remove corresponding file
                path = pref.getNoCheck(pref.CONFIG_SCRIPT_PATH)
                try:
                    os.remove(path + fileName)
                except OSError as err:
                    e = pref.getError(pref.ERROR_FILE_NOT_FOUND, args = (fileName))

        return e

    # overriding abstract method
    @staticmethod
    def editEntry(entry: Script):
        '''
        Updates a row in the script SQL table based on the entry object passed. 
        Overwrites all attributes of the row with the values of the entry object.
        Overwrites row based on the ID of the entry object.
        @param 
            entry: Script - Script object, must have ID != None or error will be thrown
        @return 
            e - most recent error when executing function or Success if no error occurs
            s - Script object corresponding to row updated in SQL table. Should be the 
                same as entry passed to function if no error occured
        '''
        s = entry

        if(entry.ID == None):
            e = pref.getError(pref.ERROR_NO_ID_PROVIDED, args=("editEntry", "Script"))

        else:
            command = """UPDATE s SET """
            for attr, value in entry.__dict__.items():
                if (attr == "ID"):
                    pass
                else:
                    command = command + str(attr)
                    if(value == None):
                        command = command + """ = NULL"""
                    elif attr[0:2] == "dt":
                        command = command + """ = """ + """\"""" + str(value.strftime('%Y-%m-%d %H:%M:%S.%f')) + """\""""
                    elif isinstance(value, str):
                        command = command + """ = """ + """\"""" + str(value) + """\""""
                    else:
                        command = command + """ = """ + str(value)
                    command = command + """, """
            command = command[:-2] #remove last ' ,'
            command = command + """ WHERE ID = """ + str(entry.ID) + """;"""

            e = sqlFuncs.exeCommand(command, "editEntry", "Script")

            if(e == pref.getError(pref.ERROR_SUCCESS)):
                command2 = """SELECT * FROM s WHERE ID = """ + str(entry.ID) + """;"""
                e, row = sqlFuncs.getRow(command2, "editEntry", "Script")
                if(e == pref.getError(pref.ERROR_SUCCESS)):
                    e, s = tupleToScript(row, "editEntry")

        return e, s

######################################################################################################
########################## Functions relating to Script/ScriptTable classes ##########################
######################################################################################################

def tupleToScript(tup: tuple, commandName: str):
    '''
    Seperates a tuple of script object parameter values to init a script object. 
    Does error checking to confirm that the tuple contains elements for all attributes of the script class.
    Casts all attributes to correct type. 
    @param 
        tup - a tuple containing values for every parameter of the Script class
    @return 
        e - most recent error when executing function or Success if no error occurs 
        s - the Script object created
    '''
    # ID: int, name: str, fileName: str, author: int, desc: str, dtCreated: datetime.datetime,dtModified: datetime.datetime, size: float, isAdmin: bool
    e = pref.getError(pref.ERROR_SUCCESS)
    s = None
    if(tup == None):
        e = pref.getError(pref.ERROR_SQL_RETURN_MISSING_ATTR, args=(commandName, "Script", 0, 9))
    elif(len(tup) != 9):
        e = pref.getError(pref.ERROR_SQL_RETURN_MISSING_ATTR, args=(commandName, "Script", len(tup), 9))
    else:
        try:
            if(tup[0] == None):
                ID = None
            else:
                ID = int(tup[0])

            if(tup[1] == None):
                name = None
            else:
                name = str(tup[1])

            if(tup[2] == None):
                fileName = None
            else:
                fileName = str(tup[2])

            if(tup[3] == None):
                author = None
            else:
                author = int(tup[3])

            if(tup[4] == None):
                desc = None
            else:
                desc = str(tup[4])

            if(tup[5] == None):
                dtCreated = None
            else:
                dtCreated = datetime.datetime.strptime(tup[5], '%Y-%m-%d %H:%M:%S.%f')

            if(tup[6] == None):
                dtModified = None
            else:
                dtModified = datetime.datetime.strptime(tup[6], '%Y-%m-%d %H:%M:%S.%f')

            if(tup[7] == None):
                size = None
            else:
                size = int(tup[7])

            if(tup[8] == None):
                isAdmin = None
            else:
                isAdmin = bool(tup[8])

            s = Script(ID, name, fileName, author, desc, dtCreated, dtModified, size, isAdmin)
        except ValueError as err:
            e = pref.getError(pref.ERROR_SQL_RETURN_CAST, args=(commandName, "Script", err))
            s = None

    return e, s