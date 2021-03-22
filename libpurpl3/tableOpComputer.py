import datetime
import libpurpl3.preferences as pref
import libpurpl3.tableOp as tableOp
import libpurpl3.sqlFuncs as sqlFuncs
import sqlite3

class Computer(tableOp.Entry):
    #TODO add default values
    # overriding abstract method
    def __init__(self, ID: int, userID: int, name: str, nickName: str, desc: str, username: str, IP: str, dtCreated: datetime.datetime,
                 dtModified: datetime.datetime, asAdmin: bool):
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
                       id INTEGER,
                       userId INTEGER,
                       name CHAR(256),
                       nickName CHAR(256),
                       desc CHAR(1024),
                       IP CHAR(256),
                       dtCreated DATETIME,
                       dtModified DATETIME,
                       asAdmin BOOL,
                       PRIMARY KEY(id),
                       FOREIGN KEY (userId) REFERENCES u(id)
                    );"""
        e = sqlFuncs.createTable(command)
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
        skelComp = Computer(ID, 0, "RachelsComputer", "RaquelsComp", "Rachel's computer description",
                              "root","127.0.0.1", datetime.datetime.now(), datetime.datetime.now(), False)
        return pref.getError(pref.ERROR_SUCCESS), skelComp

    # overriding abstract method
    @staticmethod
    def getAll():
        '''
        #TODO
        *add description*.
        @param *add param*.
        @return *add return*.
        '''
        skelComp1 = Computer(0, 0, "RachelsComputer1", "RaquelsComp1", "Rachel's computer description 1",
                            "root","127.0.0.1", datetime.datetime.now(), datetime.datetime.now(), False)
        skelComp2 = Computer(1, 0, "RachelsComputer2", "RaquelsComp2", "Rachel's computer description 2",
                            "larry","127.0.0.1", datetime.datetime.now(), datetime.datetime.now(), False)
        compTup = (skelComp1, skelComp2)
        return pref.getError(pref.ERROR_SUCCESS), compTup

    # overriding abstract method
    @staticmethod
    def createEntry(values: tuple):
        '''
        #TODO
        *add description*.
        @param *add param*.
        @return *add return*.
        '''
        # TODO error check what is passed to function (in terms of types?)
        skelComp = Computer(values[0], values[1], values[2], values[3], values[4], values[5], values[6], values[7],
                            values[8],values[9])
        return pref.getError(pref.ERROR_SUCCESS), skelComp

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
        if (attr == "ID" or attr == "userID"):
            return pref.getError(pref.ERROR_SUCCESS), 0
        # str
        elif (attr == "name" or attr == "nickName" or attr == "desc" or attr == "IP" or attr == "username"):
            return pref.getError(pref.ERROR_SUCCESS), ""
        # datetime
        elif (attr == "dtCreated" or attr == "dtModified"):
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
        skelComp = Computer(0, 0, "RachelsComputer1", "RaquelsComp1", "Rachel's computer description 1",
                             "root","127.0.0.1", datetime.datetime.now(), datetime.datetime.now(), False)
        return pref.getError(pref.ERROR_SUCCESS), skelComp

    # overriding abstract method
    @staticmethod
    def add(entry: Computer):
        '''
        #TODO
        *add description*.
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
        skelComp = Computer(0, 0, "RachelsComputer1", "RaquelsComp1", "Rachel's computer description 1",
                             "root","127.0.0.1", datetime.datetime.now(), datetime.datetime.now(), False)
        return pref.getError(pref.ERROR_SUCCESS), skelComp
