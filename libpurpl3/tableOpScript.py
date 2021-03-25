import datetime
from datetime import datetime as dt
import libpurpl3.preferences as pref 
import libpurpl3.tableOp as tableOp
import libpurpl3.sqlFuncs as sqlFuncs
import sqlite3
import os

class Script(tableOp.Entry):
    #TODO add default values
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
                       id INTEGER PRIMARY KEY,
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
        # e = sqlFuncs.createTable(command, "Script")
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
        #TODO
        *add description*.
        @param *add param*.
        @return *add return*.
        '''
        skelScript = Script(ID, "SkeletonScriptName", "SkeletonScriptName.py", 1, "Skeleton Script Description", datetime.datetime.now(), datetime.datetime.now(), 0, False)
        return pref.getError(pref.ERROR_SUCCESS), skelScript

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
            Error - error object indicating if any error was encountered when creating the script object 
            script - script object created
        '''
        # id will be set when object is added to table
        id = None
        # set dtCreated
        dtCreated = dt.now()
        # set dtModified (will be same as dtCreated initially)
        dtModified = dtCreated
        # set size
        filePath = pref.getNoCheck("SCRIPT_PATH") + fileName
        fileStats = os.stat(filePath)
        fileSizeMB = fileStats.st_size / (1024 * 1024)
        
        # create script object
        script = Script(None, name, fileName, author, desc, dtCreated, dtModified, fileSizeMB, isAdmin)
        return pref.getError(pref.ERROR_SUCCESS), script #FIXME - error is redundant, take out???

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
        if(attr == "ID" or attr == "author"):
            return pref.getError(pref.ERROR_SUCCESS), 0
        #str
        elif(attr == "name" or attr == "fileName" or attr == "desc"):
            return pref.getError(pref.ERROR_SUCCESS), ""
        # datetime
        elif(attr == "dtCreated" or attr == "dtModified"):
            return pref.getError(pref.ERROR_SUCCESS), datetime.datetime.now()
        #float
        elif(attr == "size"):
            return pref.getError(pref.ERROR_SUCCESS), 0
        #bool
        elif(attr == "isAdmin"):
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
        skelScript = Script(0, "SkeletonScriptName", "SkeletonScriptName.py", 1, "Skeleton Script Description", datetime.datetime.now(), datetime.datetime.now(), 0, False)
        return pref.getError(pref.ERROR_SUCCESS), skelScript

    # overriding abstract method
    @staticmethod
    def add(entry: Script): 
        '''
        #TODO
        Must take script object from createEntry call.
        @param *add param*.
        @return *add return*.
        '''
        ID: int = 0
        return pref.getError(pref.ERROR_SUCCESS), ID
        

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


