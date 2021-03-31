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
                param = param + (value.strftime('%Y-%m-%d %H:%M:%S.%f'), )
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
    def checkLogin(username: str, password: str)->int:
        '''
        Checks username and password against database.
        Will return -1 if username is not in database or password given does not match database password
        @param 
            username: str - the username of the user cannot contain " " or ";"
            password: str - a hashed password to check against database
        @return 
            userID: int - userID corresponding to username and password passed or -1 if failed
        '''
        userID = -1
        command = """SELECT * FROM u WHERE (username = \"""" + str(username) + """\" AND password = \"""" + str(password) + """\");"""
        e, rows = sqlFuncs.getAllRows(command, "checkLogin", "User")
        if(e == pref.getError(pref.ERROR_SUCCESS)):
            if(len(rows) == 1): # if a  single user was found
                userID = rows[0][0] # take first (and only) row  =and first element (userID) of this row

        return userID

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
        u = None
        command = """SELECT * FROM u WHERE ID = """ + str(ID) + """;"""
        e, uTuple = sqlFuncs.getRow(command, "getByID", "User")
        if (e == pref.getError(pref.ERROR_SUCCESS)):
            e, u = tupleToUser(uTuple, "getByID")
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
        if(e == pref.getError(pref.ERROR_SUCCESS)):
            if (rows != None):
                for row in rows:
                    e, u = tupleToUser(row, "getAll")
                    if(e == pref.getError(pref.ERROR_SUCCESS)):
                        uList.append(u)

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
        val = None
        command = """SELECT (""" + attr + """) FROM u WHERE ID = """ + str(ID) + """;"""
        e, uTuple = sqlFuncs.getRow(command, "getAttrByID", "User")
        if (e == pref.getError(pref.ERROR_SUCCESS)):
            if(uTuple == None):
                e = pref.getError(pref.ERROR_SQL_RETURN_MISSING_ATTR, args=("getAttrByID", "User", 0, 1))
            elif(len(uTuple) != 1):
                e = pref.getError(pref.ERROR_SQL_RETURN_MISSING_ATTR, args=("getAttrByID", "User", len(uTuple), 1))
            else:
                val = uTuple[0]
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
        ID = None
        command = """ INSERT INTO u (id, username, password, dtCreated, dtModified, admin) VALUES (NULL, ?, ?, ?, ?, ?)"""
        data = entry.paramToList()
        e, ID = sqlFuncs.insert(command, data, "add", "User")
        entry.ID = ID # access ID through entry object after executing this function
        return e

    # overriding abstract method
    @staticmethod
    def delete(ID: int):
        '''
        Removes a user entry from the database based on it's ID. 
        @param 
            ID: int - primary key of user
        @return 
            e - most recent error when executing function or Success if no error occurs
        '''
        command = """DELETE FROM u WHERE ID = """ + str(ID) + """;"""
        e = sqlFuncs.exeCommand(command, "delete", "User")

        return e


    # overriding abstract method
    @staticmethod
    def editEntry(entry: User):
        '''
        Updates a row in the user SQL table based on the entry object passed. 
        Overwrites all attributes of the row with the values of the entry object.
        Overwrites row based on the ID of the entry object.
        @param 
            entry: User - User object, must have ID != None or error will be thrown
        @return 
            e - most recent error when executing function or Success if no error occurs
            u - User object corresponding to row updated in SQL table. Should be the 
                same as entry passed to function if no error occured
        '''
        u = entry

        if(entry.ID == None):
            e = pref.getError(pref.ERROR_NO_ID_PROVIDED, args=("editEntry", "User"))

        else:
            command = """UPDATE u SET """
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

            e = sqlFuncs.exeCommand(command, "editEntry", "User")

            if(e == pref.getError(pref.ERROR_SUCCESS)):
                command2 = """SELECT * FROM u WHERE ID = """ + str(entry.ID) + """;"""
                e, row = sqlFuncs.getRow(command2, "editEntry", "User")
                if(e == pref.getError(pref.ERROR_SUCCESS)):
                    e, u = tupleToUser(row, "editEntry")

        return e, u


######################################################################################################
############################ Functions relating to User/UserTable classes ############################
######################################################################################################

def tupleToUser(tup: tuple, commandName: str):
    '''
    Seperates a tuple of User object parameter values to init a User object. 
    Does error checking to confirm that the tuple contains elements for all attributes of the User class.
    Casts all attributes to correct type. 
    @param 
        tup - a tuple containing values for every parameter of the User class
    @return 
        e - most recent error when executing function or Success if no error occurs 
        u - the User object created
    '''
    # ID: int, username: str, password: str, dtCreated: datetime.datetime,
    # dtModified: datetime.datetime, admin: bool
    e = pref.getError(pref.ERROR_SUCCESS)
    u = None
    if(tup == None):
        e = pref.getError(pref.ERROR_SQL_RETURN_MISSING_ATTR, args=(commandName, "User", 0, 6))
    elif(len(tup) != 6):
        e = pref.getError(pref.ERROR_SQL_RETURN_MISSING_ATTR, args=(commandName, "User", len(tup), 6))
    else:
        try:
            if(tup[0] == None):
                ID = None
            else:
                ID = int(tup[0])

            if(tup[1] == None):
                username = None
            else:
                username = str(tup[1])

            if(tup[2] == None):
                password = None
            else:
                password = str(tup[2])

            if(tup[3] == None):
                dtCreated = None
            else:
                dtCreated = datetime.datetime.strptime(tup[3], '%Y-%m-%d %H:%M:%S.%f')

            if(tup[4] == None):
                dtModified = None
            else:
                dtModified = datetime.datetime.strptime(tup[4], '%Y-%m-%d %H:%M:%S.%f')

            if(tup[5] == None):
                isAdmin = None
            else:
                isAdmin = bool(tup[5])

            u = User(ID, username, password, dtCreated, dtModified, isAdmin)
        except ValueError as err:
            e = pref.getError(pref.ERROR_SQL_RETURN_CAST, args=(commandName, "User", err))
            u = None

    return e, u