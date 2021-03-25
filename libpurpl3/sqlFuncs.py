import sqlite3
from sqlite3 import Error
import libpurpl3.preferences as pref 

# Need sqlite3 version 3.6+ : https://charlesleifer.com/blog/compiling-sqlite-for-use-with-python-applications/

def exeCommand(command: str, commandName: str, tableName:type):
    e = pref.getError(pref.ERROR_SUCCESS)
    try:
        con = sqlite3.connect(pref.getNoCheck("DB_PATH"))
        con.execute('PRAGMA foreign_keys = 1') #enable foreign keys
        try:
            cur = con.cursor()
            cur.execute(command)
        except Error as err:
            print(err)
            e = pref.getError(pref.ERROR_EXECUTE_SQLITE3_COMMAND, args=(commandName, tableName, err))
    except Error as err:
        print(err)
        e = pref.getError(pref.ERROR_CREATE_SQLITE3_CONNECTION, args = (command, tableName, err))

    return e
