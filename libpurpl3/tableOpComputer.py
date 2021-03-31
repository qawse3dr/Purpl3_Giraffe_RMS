import datetime
from datetime import datetime as dt
import libpurpl3.preferences as pref
import libpurpl3.tableOp as tableOp
import libpurpl3.sqlFuncs as sqlFuncs
import sqlite3

class Computer(tableOp.Entry):
    #TODO add default values
    # overriding abstract method
    def __init__(self, ID: int, userID: int, name: str, nickName: str, desc: str, username: str, IP: str, dtCreated: datetime.datetime,
                 dtModified: datetime.datetime, asAdmin: bool):
        '''
        Creates computer object. Contains all info on a provisioned computer.
        @param 
            ID: int - unique identifier automatically generated when script is added to sql table. Will be None until script is added to table.
            userID: int - primary key of user table to indicate which user provisioned this computer 
            name: str - predefined name of computer
            nickName: str - user defined name for computer 
            desc: str - user defined computer description 
            username: str - username of user being accessed on computer 
            IP: str - IP address of computer
            dtCreated: datetime.datetime - dateTime when createEntry is called for the computer
            dtModified: datetime.datetime - dateTime when createEntry is called for the computer or when editEntry is called
            asAdmin: bool - whether or not user is accessing computer as admin
        @return 
            None.
        '''
        self.ID = ID
        self.userID = userID
        self.name = name
        self.nickName = nickName
        self.desc = desc
        self.username = username
        self.IP = IP
        self.dtCreated = dtCreated
        self.dtModified = dtModified
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
            "userID": str(self.userID),
            "name": str(self.name),
            "nickName": str(self.nickName),
            "desc": str(self.desc),
            "username": str(self.username),
            "IP": str(self.IP),
            "dtCreated": str(self.dtCreated),
            "dtModified": str(self.dtModified),
            "asAdmin": str(self.asAdmin)
        }

    def paramToList(self):
        '''
        Returns all the parameters of a computer object as a tuple that can be used for SQL calls.
        Omits id from tuple as id will be automatically generated using AUTOINCREMENT when the script object is added to the table.
        @param 
            None.
        @return 
            param - tuple of all attribute's values for computer object, omitting ID
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


class ComputerTable(tableOp.Table):
    # overriding abstract method
    @staticmethod
    def createTable():
        '''
        creates an empty SQL table for scripts
        @param None.
        @return errorCode: Error
        '''
        command = """CREATE TABLE IF NOT EXISTS c (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       userId INTEGER,
                       name CHAR(256),
                       nickName CHAR(256),
                       desc CHAR(1024),
                       username CHAR(256),
                       IP CHAR(256),
                       dtCreated DATETIME,
                       dtModified DATETIME,
                       asAdmin BOOL,
                       FOREIGN KEY (userId) REFERENCES u(id)
                    );"""
        e = sqlFuncs.exeCommand(command, "createTable", "Computer")
        # e = sqlFuncs.createTable(command, "Computer")
        return e

    # overriding abstract method
    @staticmethod
    def deleteTable():
        '''
        Removes the computer SQL table from the database. Used for testing principally.
        @param None.
        @return e - Error code, returns success if no error occurs.
        '''
        command = """DROP TABLE c;
                  """
        e = sqlFuncs.exeCommand(command, "deleteTable", "Computer")
        return e

    # overriding abstract method
    @staticmethod
    def getByID(ID: int):
        '''
        Retrieves an entry from the computer SQL table based on primary key - ID
        @param 
            ID - primary key of computer
        @return 
            e - error created during execution of function or Success if no error occurs
            s - the entry retrieved from the SQL table as a Computer object
        '''
        c = None
        command = """SELECT * FROM c WHERE ID = """ + str(ID) + """;"""
        e, cTuple = sqlFuncs.getRow(command, "getByID", "Computer")
        if(e == pref.getError(pref.ERROR_SUCCESS)):
            e, c = tupleToComputer(cTuple, "getByID")
        return e, c

    # overriding abstract method
    @staticmethod
    def getAll():
        '''
        Retreives all entries from the computer SQL table and returns them as a list of computer objects
        @param 
            None.
        @return 
            cList - list of computer objects.
        '''
        command = """SELECT * FROM c;"""
        e, rows = sqlFuncs.getAllRows(command, "getAll", "Computer")
        cList = []
        if(e == pref.getError(pref.ERROR_SUCCESS)):
            for row in rows:
                print(row)
                e, c = tupleToComputer(row, "getAll")
                if(e == pref.getError(pref.ERROR_SUCCESS)):
                    cList.append(c)

        return e, cList

    # overriding abstract method
    @staticmethod
    def createEntry(userID: int, name: str, nickName: str, desc: str, username: str, IP: str, asAdmin: bool):
        '''
        Creates a computer object. Some parameters must be passed in, some will be calculated 
        in this function and some can only be filled when the computer is added to the SQL 
        table (these parameters will be set to None until the computer is added to the SQL table).
        @param 
            userID: int - primary key of user table to indicate which user provisioned this computer 
            name: str - predefined name of computer
            nickName: str - user defined name for computer 
            desc: str - user defined computer description 
            username: str - username of user being accessed on computer 
            IP: str - IP address of computer
            asAdmin: bool - whether or not user is accessing computer as admin
        @return 
            computer - computer object created
        '''
        # id will be set when object is added to table
        id = None
        # set dtCreated
        dtCreated = dt.now()
        # set dtModified (will be same as dtCreated initially)
        dtModified = dtCreated
        # create computer object
        computer = Computer(id, userID, name, nickName, desc, username, IP, dtCreated, dtModified, asAdmin)
        return computer 

    # overriding abstract method
    @staticmethod
    def getAttrByID(attr: str, ID: int):
        '''
        Retrieves a specified attrubute from an entry of the computer SQL table based on primary key - ID
        @param 
            attr - one of the columns of the computer table
            ID - primary key of computer
        @return 
            e - error created during execution of function or Success if no error occurs
            s - the specified attribute's value from the entry retrieved from the SQL table 
        '''
        val = None
        command = """SELECT (""" + attr + """) FROM c WHERE ID = """ + str(ID) + """;"""
        e, cTuple = sqlFuncs.getRow(command, "getAttrByID", "Computer")
        if(e == pref.getError(pref.ERROR_SUCCESS)):
            val = cTuple[0]
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
        skelComp = Computer(0, 0, "RachelsComputer1", "RaquelsComp1", "Rachel's computer description 1",
                             "root","127.0.0.1", datetime.datetime.now(), datetime.datetime.now(), False)
        return pref.getError(pref.ERROR_SUCCESS), skelComp

    # overriding abstract method
    @staticmethod
    def add(entry: Computer):
        '''
        Takes a computer object (which has not yet been added to the computer SQL table), 
            adds it to the table and updates computer object's ID (ID is automatically 
            generated using sqlite AUTOINCREMENT) 
        This function is meant to take a computer object generated from a call to the 
            createEntry function.
        @param 
            entry - object of class Computer
        @return 
            e - most recent error when executing function or Success if no error occurs
        '''
        ID = None
        command = """ INSERT INTO c (id, userID, name, nickName, desc, username, IP, dtCreated, dtModified, asAdmin) VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
        data = entry.paramToList()
        e, ID = sqlFuncs.insert(command, data, "add", "Computer")
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
    def editEntry(entry: Computer):
        '''
        Updates a row in the computer SQL table based on the entry object passed. 
        Overwrites all attributes of the row with the values of the entry object.
        Overwrites row based on the ID of the entry object.
        @param 
            entry: Computer - Computer object, must have ID != None or error will be thrown
        @return 
            e - most recent error when executing function or Success if no error occurs
            c - Computer object corresponding to row updated in SQL table. Should be the 
                same as entry passed to function if no error occured
        '''
        c = entry

        if(entry.ID == None):
            e = pref.getError(pref.ERROR_NO_ID_PROVIDED, args=("editEntry", "Computer"))

        else:
            command = """UPDATE c SET """
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
            print(command)

            e = sqlFuncs.exeCommand(command, "editEntry", "Computer")

            if(e == pref.getError(pref.ERROR_SUCCESS)):
                command2 = """SELECT * FROM c WHERE ID = """ + str(entry.ID) + """;"""
                e, row = sqlFuncs.getRow(command2, "editEntry", "Computer")
                if(e == pref.getError(pref.ERROR_SUCCESS)):
                    e, c = tupleToComputer(row, "editEntry")

        return e, c

######################################################################################################
######################## Functions relating to Computer/ComputerTable classes ########################
######################################################################################################
def tupleToComputer(tup: tuple, commandName: str):
    '''
    Seperates a tuple of Computer object parameter values to init a Computer object. 
    Does error checking to confirm that the tuple contains elements for all attributes of the Computer class.
    Casts all attributes to correct type. 
    @param 
        tup - a tuple containing values for every parameter of the Computer class
    @return 
        e - most recent error when executing function or Success if no error occurs 
        c - the Computer object created
    '''
    # ID: int, name: str, fileName: str, author: int, desc: str, dtCreated: datetime.datetime,dtModified: datetime.datetime, size: float, isAdmin: bool
    e = pref.getError(pref.ERROR_SUCCESS)
    if(len(tup) != 10):
        e = pref.getError(pref.ERROR_SQL_RETURN_MISSING_ATTR, args=(commandName, "Computer", len(tup), 10))
        c = None
    else:
        try:
            # ID: int, userID: int, name: str, nickName: str, desc: str, username: str, IP: str, 
            # dtCreated: datetime.datetime, dtModified: datetime.datetime, asAdmin: bool
            if(tup[0] == None):
                ID = None
            else:
                ID = int(tup[0])

            if(tup[1] == None):
                userID = None
            else:
                userID = int(tup[1])

            if(tup[2] == None):
                name = None
            else:
                name = str(tup[2])

            if(tup[3] == None):
                nickName = None
            else:
                nickName = str(tup[3])

            if(tup[4] == None):
                desc = None
            else:
                desc = str(tup[4])

            if(tup[5] == None):
                username = None
            else:
                username = str(tup[5])

            if(tup[6] == None):
                IP = None
            else:
                IP = str(tup[6])

            if(tup[7] == None):
                dtCreated = None
            else:
                dtCreated = datetime.datetime.strptime(tup[7], '%Y-%m-%d %H:%M:%S.%f')

            if(tup[8] == None):
                dtModified = None
            else:
                dtModified = datetime.datetime.strptime(tup[8], '%Y-%m-%d %H:%M:%S.%f')

            if(tup[9] == None):
                asAdmin = None
            else:
                asAdmin = bool(tup[9])

            c = Computer(ID, userID, name, nickName, desc, username, IP, dtCreated, dtModified, asAdmin)
        except ValueError as err:
            e = pref.getError(pref.ERROR_SQL_RETURN_CAST, args=(commandName, "Computer", err))
            c = None

    return e, c