#!/bin/python
'''
Command Line tool for purple_rms application.
Use python Purpl3_CMD --help for more info
@author Larry (qawse3dr) Milne
'''

import argparse
import sqlite3
import hashlib
import libpurpl3.preferences as pref
import libpurpl3.tableOpComputer as computerTable
import libpurpl3.tableOp as Table
import libpurpl3.tableOpScript as scriptTable
import libpurpl3.tableOpScriptLog as scriptLogTable
import libpurpl3.tableOpUser as userTable
import libpurpl3.sshServer as ssh


pref.setConfigFile("config.yaml")


def createComputer(obj: str):
  '''
  Creates a computer from either a passed string
  or if None will ask user for values
  @param obj string created by --obj \"userID, name, desc, username, password, IP, asAdmin(0,1) \"
  @return a computer object
  '''

  #Ask user for input
  values = [None]*8
  if(obj == None):
    values[0] = int(input("Enter UserID: "))
    values[1] = "name"
    values[2] = input("Enter computer name: ")
    values[3] = input("Enter Description: ")
    values[4] = input("Enter Username: ")
    values[5] = input("Enter Password: ")
    values[6] = input("Enter IPv4: ")
    values[7] = bool(int(input("Enter if admin(0, 1): ")))
  #input given in obj
  else:
    values = obj.split(",")
    for x in range(len(values)):
      values[x] = values[x].strip()

  #Tries to add sshkey to computer
  err = ssh.sshConnection.addNewComputer(values[6],values[4],values[5])
  if err == pref.Success:
    return computerTable.ComputerTable.createEntry(int(values[0]),values[1],values[2],values[3],values[4],values[6],bool(int(values[7])))
  else: #Failed connection with computer
    print("Failed to add computer")
    print(err)
    return None


def createUser(obj: str):
  '''
  Creates a user from either a passed string
  or if None will ask user for values
  @param obj string created by --obj \" username, password, isAdmin(1 or 0)\"
  @return a user object
  '''
  
  #Asks user for input
  values = [None]*3
  if(obj == None):
    values[0] = input("Enter Username: ")
    values[1] = input("Enter Password: ")
    values[2] = bool(int(input("Enter if admin(0, 1): ")))
  else:
  #gets input from user
    values = obj.split(",")
    for x in range(len(values)):
      values[x] = values[x].strip()

  #hash password
  values[1] = hashlib.sha256(values[1].encode()).hexdigest()

  #return user
  return userTable.UserTable.createEntry(values[0],values[1],bool(int(values[2])))

def createScript(obj: str):
  '''
  Creates a script from either a passed string
  or if None will ask user for values
  @param obj string created by --obj \"name, fileName.sh, userID, desc, isAdmin(1,0) \"
  @return a user object
  '''
  values = [None]*5
  if(obj == None):
    values[0] = input("Enter name: ")
    values[1] = input("filename: ")
    values[2] = int(input("Enter author ID: "))
    values[3] = input("Enter Description: ")
    values[4] = bool(int(input("Enter if admin(0, 1): ")))
  else:
    values = obj.split(",")
    for x in range(len(values)):
      values[x] = values[x].strip()

  return scriptTable.ScriptTable.createEntry(values[0], values[1], int(values[2]), values[3],bool(int(values[4])))


#params for command line tool
parser = argparse.ArgumentParser(description="Command Line tool for purple_rms application.", formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('--create', action='store_true')
parser.add_argument("--add", nargs="?", help="Adds element to db (computer, script, user)")
parser.add_argument("--edit",nargs="?", help="Edits element in db by id (computer, script, user)")
parser.add_argument("--del", nargs="?", help="Delete element in db by id (computer, script user)")
parser.add_argument("--display", nargs="?", help="Displays db's table name (computer, script, user, scriptLogs)")
parser.add_argument("--id", nargs="?", help="The id of an element")
parser.add_argument("--obj", nargs="?", help="The computer object used example\n"
  "--add computer --obj \"userID, name, desc, username, password, IP, asAdmin(0,1) \"\n" +
  "--add script --obj \"name, fileName.sh, userID, desc, isAdmin(1,0) \"\n" +
  "--add users --obj \" username, password, isAdmin(1 or 0)\"" )
  

#parse args and prints out vars
args = parser.parse_args()
val = vars(args)
print(val)


#gets db name and connection
dbName = pref.getNoCheck(pref.CONFIG_DB_PATH)
con = sqlite3.connect(dbName)


#Creates tables
if(val["create"]):
  e = scriptLogTable.ScriptLogTable.createTable()
  e = scriptTable.ScriptTable.createTable()
  e = computerTable.ComputerTable.createTable()
  e = userTable.UserTable.createTable()
  exit(0)

#Adds to table
if(val["add"] != None):
  if val["add"] == "computer":
    entry = createComputer(val["obj"])
    if(entry):
      computerTable.ComputerTable.add(entry)
  elif val["add"] == "script":
    entry = createScript(val["obj"])
    if(entry):
      scriptTable.ScriptTable.add(entry)
  elif val["add"] == "user":
    entry = createUser(val["obj"])
    if(entry):
      userTable.UserTable.add(entry)
  else:
    print("TABLE COULD NOT BE FOUND")
#edit TODO implement
elif(val["edit"] != None):
  pass

#deletes by id
elif(val["del"] != None):
  id = None
  #gets id from user
  if(val["id"] == None):
    id = input("Enter The ID")
  else: #given in cmdline args
    id = val["id"]

  #deletes from table 
  if val["del"] == "computer":
    computerTable.ComputerTable.delete(int(id.strip()))
  elif val["del"] == "script":
    scriptTable.ScriptTable.delete(int(id.strip()))
  elif val["del"] == "user":
    userTable.UserTable.delete(int(id.strip()))
  elif val["del"] == "scriptLogs":
    scriptLogTable.ScriptLogTable.delete(int(id.strip()))
  else:
    print("TABLE COULD NOT BE FOUND")

#display tables
elif(val["display"] != None):
  if val["display"] == "computer":
    cursor = con.cursor()
    cursor.execute("SELECT * FROM c")
    print("DISPLAY COMPUTER")
    print(list(map(lambda x: x[0], cursor.description)))
    print(cursor.fetchall())
    cursor.close()
  elif val["display"] == "script":
    cursor = con.cursor()
    cursor.execute("SELECT * FROM s")
    print("DISPLAY SCRIPT")
    print(list(map(lambda x: x[0], cursor.description)))
    for row in cursor.fetchall():
      print(row)
    cursor.close()
  elif val["display"] == "scriptLog":
    cursor = con.cursor()
    cursor.execute("SELECT * FROM sl")
    print("DISPLAY SCRIPT LOG")
    print(list(map(lambda x: x[0], cursor.description)))
    print(cursor.fetchall())
    cursor.close()
  elif val["display"] == "user":
    cursor = con.cursor()
    cursor.execute("SELECT * FROM u")
    print("DISPLAY USER")
    print(list(map(lambda x: x[0], cursor.description)))
    for row in cursor.fetchall():
      print(row)
    cursor.close()
  else:
    print("TABLE COULD NOT BE FOUND")

#close db connection
con.close()