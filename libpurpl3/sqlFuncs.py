import sqlite3
from sqlite3 import Error
import libpurpl3.preferences as pref 

# Need sqlite3 version 3.6+ : https://charlesleifer.com/blog/compiling-sqlite-for-use-with-python-applications/

def exeCommand(command: str, commandName: str, tableName:type):
    '''
    Executes a command in the SQL database which requires no extra data passed to the call and expects no return.
    @param 
        command - SQL command as a string
        commandName - name of the function calling exeCommand. Used for error creation.
        tableName - name of the table command is being executed. Used for error creation. In full word form i.e. script, not s.
    @return 
        None.
    '''
    e = pref.getError(pref.ERROR_SUCCESS)
    try: # attempt to create connection
        con = sqlite3.connect(pref.getNoCheck(pref.CONFIG_DB_PATH))
        con.execute('PRAGMA foreign_keys = 1') #enable foreign keys
        try: # attempt to execute some command
            cur = con.cursor()
            cur.execute(command)
            con.commit()
        except Error as err: # command execution failed
            print(err)
            e = pref.getError(pref.ERROR_EXECUTE_SQLITE3_COMMAND, args=(commandName, tableName, err)) # return error with specific info
        con.close()
    except Error as err: # connection creation failed
        print(err)
        e = pref.getError(pref.ERROR_CREATE_SQLITE3_CONNECTION, args = (command, tableName, err)) # return error with specific info

    return e

def insert(command: str, data: tuple, commandName: str, tableName:type):
    '''
    Executes an insert command in the SQL database which requires extra data and returns the automatically generated primary key ID.
    @param 
        command - SQL command as a string
        data - tuple of data being inserted that is not NULL
        commandName - name of the function calling exeCommand. Used for error creation.
        tableName - name of the table command is being executed. Used for error creation. In full word form i.e. script, not s.
    @return 
        ret : int - ID assigned to inserted row
    '''
    e = pref.getError(pref.ERROR_SUCCESS)
    ret = None
    try: # attempt to create connection
        con = sqlite3.connect(pref.getNoCheck(pref.CONFIG_DB_PATH))
        con.execute('PRAGMA foreign_keys = 1') #enable foreign keys
        try: # attempt to execute insert command
            cur = con.cursor()
            cur.execute(command, data)
        except Error as err: # command execution failed
            print(err)
            e = pref.getError(pref.ERROR_EXECUTE_SQLITE3_COMMAND, args=(commandName, tableName, err)) # return error with specific info
        
        try: # attempt to get return data
            command2 = """SELECT last_insert_rowid();"""
            cur.execute(command2)
            row = cur.fetchone()
            if row != None:
                ret = row[0]
            cur.close()
        except Error as err: # return gathering failed
            print(err)
            e = pref.getError(pref.ERROR_EXECUTE_SQLITE3_COMMAND, args=(commandName, tableName, err)) # return error with specific info
        con.commit()
        con.close()  
    except Error as err: # connection creation failed
        print(err)
        e = pref.getError(pref.ERROR_CREATE_SQLITE3_CONNECTION, args = (command, tableName, err)) # return error with specific info        

    return e, ret

def getRow(command: str, commandName: str, tableName:type):
    '''
    Executes a select command for a single row in the SQL database. Requires no extra data and returns the selected row.
    @param 
        command - SQL command as a string
        commandName - name of the function calling exeCommand. Used for error creation.
        tableName - name of the table command is being executed. Used for error creation. In full word form i.e. script, not s.
    @return 
        row - tuple for row selected.
    '''
    e = pref.getError(pref.ERROR_SUCCESS)
    row = None
    try: # attempt to create connection
        con = sqlite3.connect(pref.getNoCheck(pref.CONFIG_DB_PATH))
        con.execute('PRAGMA foreign_keys = 1') #enable foreign keys
        try: # attempt to do select command and get row
            cur = con.cursor()
            cur.execute(command)
            row = cur.fetchone()
            cur.close()
        except Error as err: # select failed
            print(err)
            e = pref.getError(pref.ERROR_EXECUTE_SQLITE3_COMMAND, args=(commandName, tableName, err)) # return error with specific info
        con.commit()
        con.close()
    except Error as err: # connection creation failed
        print(err)
        e = pref.getError(pref.ERROR_CREATE_SQLITE3_CONNECTION, args = (command, tableName, err)) # return error with specific info
        
    return e, row

def getAllRows(command: str, commandName: str, tableName:type):
    '''
    Executes a select command for a single row in the SQL database. Requires no extra data and returns the selected row.
    @param 
        command - SQL command as a string
        commandName - name of the function calling exeCommand. Used for error creation.
        tableName - name of the table command is being executed. Used for error creation. In full word form i.e. script, not s.
    @return 
        row - tuple for row selected.
    '''
    e = pref.getError(pref.ERROR_SUCCESS)
    rows = None
    try: # attempt to create connection
        con = sqlite3.connect(pref.getNoCheck(pref.CONFIG_DB_PATH))
        con.execute('PRAGMA foreign_keys = 1') #enable foreign keys
        try: # attempt to do select command and get row
            cur = con.cursor()
            cur.execute(command)
            rows = cur.fetchall()
            cur.close()
        except Error as err: # select failed
            print(err)
            e = pref.getError(pref.ERROR_EXECUTE_SQLITE3_COMMAND, args=(commandName, tableName, err)) # return error with specific info
        con.commit()
        con.close()
    except Error as err: # connection creation failed
        print(err)
        e = pref.getError(pref.ERROR_CREATE_SQLITE3_CONNECTION, args = (command, tableName, err)) # return error with specific info
        
    return e, rows