import datetime
from datetime import datetime as dt
import libpurpl3.preferences as pref
import libpurpl3.tableOp as tableOp
import libpurpl3.sqlFuncs as sqlFuncs
import sqlite3

class User(tableOp.Entry):
    #TODO add default values
    # overriding abstract method
    def __init__(self, ID: int, username: str, password: str, dtCreated: datetime.datetime,
                 dtModified: datetime.datetime, admin: bool):
        '''
        Creates user object. Contains all info on a user of the system.
        @param 
            ID: int - unique identifier automatically generated when user is added to sql table. Will be None until user is added to table.
            username: str - the given user's username
            password: str - the user's *hashed* password
            dtCreated: datetime.datetime - dateTime when createEntry is called for the user
            dtModified: datetime.datetime - dateTime when createEntry is called for the user or when editEntry is called
            admin: bool - whether or not the user has admin privledges
        @return 
            None.
        '''
        self.ID = ID
        self.username = username
        self.password = password
        self.dtCreated = dtCreated
        self.dtModified = dtModified
        self.admin = admin

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
            "username": str(self.username),
            "password": str(self.password),
            "dtCreated": str(self.dtCreated),
            "dtModified": str(self.dtModified),
            "admin": str(self.admin)
        }

    def paramToList(self):
        '''
        Returns all the parameters of a user object as a tuple that can be used for SQL calls.
        Omits id from tuple as id will be automatically generated using AUTOINCREMENT when the script object is added to the table.
        @param 
            None.
        @return 
            param - tuple of all attribute's values for user object, omitting ID
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

class UserTable(tableOp.Table):
    # overriding abstract method
    @staticmethod
    def createTable():
        '''
        creates an empty SQL table for scripts
        @param None.
        @return errorCode: Error
        '''
        command = """CREATE TABLE IF NOT EXISTS u (
                       id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                       username CHAR(256),
                       password CHAR(256),
                       dtCreated DATETIME,
                       dtModified DATETIME,
                       admin BOOL
                    );"""
        e = sqlFuncs.exeCommand(command, "createTable", "User")
        # e = sqlFuncs.createTable(command, "User")
        return e
    
    # overriding abstract method
    @staticmethod
    def deleteTable():
        '''
        Removes the user SQL table from the database. Used for testing principally.
        @param None.
        @return e - Error code, returns success if no error occurs.
        '''
        command = """DROP TABLE u;
                  """
        e = sqlFuncs.exeCommand(command, "deleteTable", "User")
        return e

    @staticmethod
    def checkLogin(userName: str, password: str)->int:
        '''
        checks username and password against db
        will return false if username is not in db or if
        password given does not match db password
        @param userName, the userName of the user cannot contain " " or ";"
        @param password, a hashed password to check against db
        @return user ID, if failed return -1
        '''
        return True

    # overriding abstract method
    @staticmethod
    def getByID(ID: int):
        '''
        Retrieves an entry from the user SQL table based on primary key - ID
        @param 
            ID - primary key of user
        @return 
            e - error created during execution of function or Success if no error occurs
            s - the entry retrieved from the SQL table as a User object
        '''
        command = """SELECT * FROM u WHERE ID = """ + str(ID) + """;"""
        e, uTuple = sqlFuncs.getRow(command, "getByID", "User")
        u = tupleToUser(uTuple)
        return e, u

    # overriding abstract method
    @staticmethod
    def getAll():
        '''
        Retreives all entries from the user SQL table and returns them as a list of user objects
        @param 
            None.
        @return 
            uList - list of user objects.
        '''
        command = """SELECT * FROM u;"""
        e, rows = sqlFuncs.getAllRows(command, "getAll", "User")
        uList = []
        for row in rows:
            print(row)
            uList.append(tupleToUser(row))

        return e, uList

    # overriding abstract method
    @staticmethod
    def createEntry(username: str, password: str, admin: bool):
        '''
        Creates a user object. Some parameters must be passed in, some will be calculated 
        in this function and some can only be filled when the user is added to the SQL 
        table (these parameters will be set to None until the user is added to the SQL table).
        @param 
            username: str - the given user's username
            password: str - the user's *hashed* password
            admin: bool - whether or not the user has admin privledges
        @return 
            user - user object created
        '''
        # id will be set when object is added to table
        id = None
        # set dtCreated
        dtCreated = dt.now()
        # set dtModified (will be same as dtCreated initially)
        dtModified = dtCreated
        # create user object
        user = User(id, username, password, dtCreated, dtModified, admin)
        return user 

    # overriding abstract method
    @staticmethod
    def getAttrByID(attr: str, ID: int):
        '''
        Retrieves a specified attribute from an entry of the user SQL table based on primary key - ID
        @param 
            attr - one of the columns of the user table
            ID - primary key of user
        @return 
            e - error created during execution of function or Success if no error occurs
            s - the specified attribute's value from the entry retrieved from the SQL table 
        '''
        command = """SELECT (""" + attr + """) FROM u WHERE ID = """ + str(ID) + """;"""
        e, uTuple = sqlFuncs.getRow(command, "getAttrByID", "User")
        return e, uTuple[0]

    # overriding abstract method
    @staticmethod
    def getWithQuery(query: str):
        '''
        #TODO
        *add description*.
        @param *add param*.
        @return *add return*.
        '''
        skelUser = User(0, "username1", "hashed password 1", datetime.datetime.now(), datetime.datetime.now(), False)
        return pref.getError(pref.ERROR_SUCCESS), skelUser

    # overriding abstract method
    @staticmethod
    def add(entry: User):
        '''
        Takes a user object (which has not yet been added to the user SQL table), 
            adds it to the table and updates user object's ID (ID is automatically 
            generated using sqlite AUTOINCREMENT) 
        This function is meant to take a user object generated from a call to the 
            createEntry function.
        @param 
            entry - object of class User
        @return 
            e - most recent error when executing function or Success if no error occurs
        '''
        ID = 0
        command = """ INSERT INTO u (id, username, password, dtCreated, dtModified, admin) VALUES (NULL, ?, ?, ?, ?, ?)"""
        data = entry.paramToList()
        e, ID = sqlFuncs.insert(command, data, "add", "User")
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
        skelUser = User(0, "username1", "hashed password 1", datetime.datetime.now(), datetime.datetime.now(), False)
        return pref.getError(pref.ERROR_SUCCESS), skelUser

def tupleToUser(tup: tuple):
    '''
    Seperates a tuple of user object parameter values to init a user object
    @param 
        tup - a tuple containing values for every parameter of the user class
    @return 
        user object
    '''
    return User(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5])