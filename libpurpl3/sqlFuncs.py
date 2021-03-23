import sqlite3
from sqlite3 import Error
import libpurpl3.preferences as pref 

def exeCommand(command: str, commandName: str, tableName:type):
    e = pref.getError(pref.ERROR_SUCCESS)
    try:
        con = sqlite3.connect("purpl3_rms.db")
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
