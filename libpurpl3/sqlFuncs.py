import sqlite3
from sqlite3 import Error
import libpurpl3.preferences as pref 

# Need sqlite3 version 3.6+ : https://charlesleifer.com/blog/compiling-sqlite-for-use-with-python-applications/

def exeCommand(command: str, commandName: str, tableName:type):
    e = pref.getError(pref.ERROR_SUCCESS)
    try: # attempt to create connection
        con = sqlite3.connect(pref.getNoCheck("DB_PATH"))
        con.execute('PRAGMA foreign_keys = 1') #enable foreign keys
        try: # attempt to execute some command
            cur = con.cursor()
            cur.execute(command)
            con.commit()
        except Error as err: # command execution failed
            print(err)
            e = pref.getError(pref.ERROR_EXECUTE_SQLITE3_COMMAND, args=(commandName, tableName, err)) # return error with specific info
    except Error as err: # connection creation failed
        print(err)
        e = pref.getError(pref.ERROR_CREATE_SQLITE3_CONNECTION, args = (command, tableName, err)) # return error with specific info
    finally:
        con.close()

    return e

def insert(command: str, data: tuple, commandName: str, tableName:type):
    e = pref.getError(pref.ERROR_SUCCESS)
    ret = None
    try: # attempt to create connection
        con = sqlite3.connect(pref.getNoCheck("DB_PATH"))
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
        except Error as err: # return gathering failed
            print(err)
            e = pref.getError(pref.ERROR_EXECUTE_SQLITE3_COMMAND, args=(commandName, tableName, err)) # return error with specific info
        finally:
            cur.close()
        
    except Error as err: # connection creation failed
        print(err)
        e = pref.getError(pref.ERROR_CREATE_SQLITE3_CONNECTION, args = (command, tableName, err)) # return error with specific info
    finally:
        con.commit()
        con.close()

    return e, ret