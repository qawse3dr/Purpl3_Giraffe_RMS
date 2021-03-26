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
            size: float - size of file containing script (in MB)
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
                param = param + (value.strftime('%Y-%m-%d %H:%M:%S'), )
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
                       CONSTRAINT author
                        FOREIGN KEY (author)
                        REFERENCES u(id)
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
        e, scriptTuple = sqlFuncs.getRow(command, "getByID", "Script")
        s = Script(scriptTuple[0], scriptTuple[1], scriptTuple[2], scriptTuple[3], scriptTuple[4], scriptTuple[5], scriptTuple[6], scriptTuple[7], scriptTuple[8])
        return e, s

    # overriding abstract method
    @staticmethod
    def getAll():
        '''
        #TODO
        *add description*.
        @param *add param*.
        @return *add return*.
        '''
        skelScript1 = Script(1, "SkeletonScriptName1", "SkeletonScriptName1.py", 1, "Skeleton Script Description 1", datetime.datetime.now(), datetime.datetime.now(), 0, False)
        skelScript2 = Script(2, "SkeletonScriptName2", "SkeletonScriptName2.py", 1, "Skeleton Script Description 2", datetime.datetime.now(), datetime.datetime.now(), 0, False)
        scriptTup = (skelScript1, skelScript2)
        return pref.getError(pref.ERROR_SUCCESS), scriptTup

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
        # id will be set when object is added to table
        id = None
        # set dtCreated
        dtCreated = dt.now()
        # set dtModified (will be same as dtCreated initially)
        dtModified = dtCreated
        # set size
        filePath = str(pref.getNoCheck(pref.CONFIG_SCRIPT_PATH)) + fileName
        fileStats = os.stat(filePath)
        fileSizeMB = fileStats.st_size / (1024 * 1024)
        
        # create script object
        script = Script(None, name, fileName, author, desc, dtCreated, dtModified, fileSizeMB, isAdmin)
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
        command = """SELECT (""" + attr + """) FROM s WHERE ID = """ + str(ID) + """;"""
        e, sTuple = sqlFuncs.getRow(command, "getAttrByID", "Script")
        return e, sTuple[0]

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
        ID = 0
        command = """ INSERT INTO s (id, name, fileName, author, desc, dtCreated, dtModified, size, isAdmin) VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?)"""
        data = entry.paramToList()
        e, ID = sqlFuncs.insert(command, data, "add", "Script")
        entry.ID = ID # access ID through entry object after executing this function
        return e

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
        skelScript = Script(0, "SkeletonScriptName", "SkeletonScriptName.py", 1, "Skeleton Script Description", datetime.datetime.now(), datetime.datetime.now(), 0, False)
        return pref.getError(pref.ERROR_SUCCESS), skelScript


