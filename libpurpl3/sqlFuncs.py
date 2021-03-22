import sqlite3
from sqlite3 import Error
import libpurpl3.preferences as pref 

def createTable(command: str, tableName:type):
    e = pref.getError(pref.ERROR_SUCCESS)
    try:
        con = sqlite3.connect("purpl3_rms.db")
        try:
            cur = con.cursor()
            cur.execute(command)
        except:
            e = pref.getError(pref.ERROR_EXECUTE_CREATE_TABLE, args=(tableName))
    except:
        e = pref.getError(pref.ERROR_SQLITE3_CONNECTION, args = ("createTable"))

    return e
