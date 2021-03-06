import libpurpl3.preferences as pref
import libpurpl3.sshServer as ssh
import libpurpl3.tableOpComputer as computerTable
import libpurpl3.tableOpScript as ScriptTable
from Purpl3_RMS import app
import datetime
import unittest
import tests.testHelpers as helper


class BaseTestCase(unittest.TestCase):
  
  #Change to reflect your machine
  username = "root"
  ip = "localhost"
  filename = "sleepScript.sh"
  #mock vars as db isn't complete yet
  computer = None 
  user = None
  script = None
  
  #reset the config before each test
  def setUp(self):
    pref.setConfigFile("tests/res/sshConfig.yaml")
    #values for mock object
    self.computer = computerTable.Computer(None,None,"name","nickName","desc",self.username, self.ip,datetime.datetime.now(),datetime.datetime.now(),False)
    self.user = None
    self.script = ScriptTable.Script(0, "script", self.filename, 0, "desc", datetime.datetime.now(), datetime.datetime.now(), 0.0, False)
  def test_connection(self):
    '''
    Basic test just testing a working connection of the ip and username given
    it will use the config.yaml configs
    '''

    #Create ssh connection
    conn = ssh.sshConnection(self.computer,self.user,self.script)

    #Connect to computer
    err = conn.connect()

    #Test for no error
    self.assertEqual(err,pref.Success)
  
  def test_connectionNoSSHKey(self):
    '''
    Basic test just testing a non-working connection of the ip and username given
    it will use a nonexistant sshkey in /DNE/NOPE
    '''

    #Create ssh connection
    conn = ssh.sshConnection(self.computer,self.user,self.script)

    #sets a nonexistant key
    pref.setAttr(pref.CONFIG_PRIVATE_SSH_KEY,"/DNE/NOPE")
    
    #Connect to computer
    err = conn.connect()

    #Test for no error
    self.assertEqual(err,pref.getError(pref.ERROR_CANT_FIND_SSH_KEY))

  def test_connectionInvalidSSHKey(self):
    '''
    Basic test just testing a non-working connection of the ip and username given
    it will use a invalid sshkey in tests/res/invalidKey
    '''

    #Create ssh connection
    conn = ssh.sshConnection(self.computer,self.user,self.script)

    #sets a nonexistant key
    pref.setAttr(pref.CONFIG_PRIVATE_SSH_KEY,"tests/res/InvalidKey")

    #Connect to computer
    err = conn.connect()

    #Test for no error
    self.assertEqual(err,pref.getError(pref.ERROR_SSH_AUTHENTICATION_FAILED))

  def test_connectionInvalidIP(self):
    '''
    Basic test just testing a non-working connection of the ip and username given
    it will use a invalid ip
    '''

    #Create ssh connection
    conn = ssh.sshConnection(self.computer,self.user,self.script)

    self.computer.IP = "192.169.100.100"

    #Connect to computer
    err = conn.connect()

    #Test for no error
    self.assertEqual(err,pref.getError(pref.ERROR_CONNECTION_FAILED))

  '''
  Only test false cases for add computer 
  due to no wanting to have a password in the source code
  '''

  def test_addComputerWrongPassword(self):
    '''tries to add a computer with the wrong password'''

    pref.setAttr(pref.CONFIG_PUBLIC_SSH_KEY,"asdfasdfasd")
    error = ssh.sshConnection.addNewComputer(self.ip,self.username,"WRONGPASSWORD!@##@!")
    self.assertEqual(error,pref.getError(pref.ERROR_SSH_AUTHENTICATION_FAILED))

  def test_addComputerEmptyPublicSSHKey(self):
    '''tries to add a computer with an empty static key'''
    pref.setAttr(pref.CONFIG_PUBLIC_SSH_KEY,"")
    error = ssh.sshConnection.addNewComputer(self.ip,self.username,"WRONGPASSWORD!@##@!")
    self.assertEqual(error,pref.getError(pref.ERROR_EMPTY_SSH_PUBLIC_KEY))

  def test_addComputerWrongIP(self):
    '''tries to add a computer with the wrong password'''

    pref.setAttr(pref.CONFIG_PUBLIC_SSH_KEY,"asdfasdfasd")
    error = ssh.sshConnection.addNewComputer("69.69.69.69",self.username,"WRONGPASSWORD!@##@!")
    self.assertEqual(error,pref.getError(pref.ERROR_CONNECTION_FAILED))
  
  def test_addComputerNonexistentUser(self):
    '''
    Tries to add a computer on a server with a user that doesn't exist
    '''
    pref.setAttr(pref.CONFIG_PUBLIC_SSH_KEY,"asdfasdfasd")
    error = ssh.sshConnection.addNewComputer(self.ip,"Wrong_User","WRONGPASSWORD!@##@!")
    self.assertEqual(error,pref.getError(pref.ERROR_SSH_AUTHENTICATION_FAILED))

  def test_addComputerScripDNE(self):
    '''
    Tries to add a computer on a server with a user that doesn't exist
    '''
    pref.setAttr(pref.CONFIG_PUBLIC_SSH_KEY,"asdfasdfasd")
    pref.setAttr(pref.CONFIG_ADD_COMPUTER_SCRIPT,"DNE")
    error = ssh.sshConnection.addNewComputer(self.ip,self.username,"WRONGPASSWORD!@##@!")
    self.assertEqual(error,pref.getError(pref.ERROR_SSH_AUTHENTICATION_FAILED))

  def test_runScript(self):
    '''
    runs basic script
    '''

    helper.createMockDB()
    user = helper.createUserAccount()
    computer = helper.createComputer()
    script = helper.createScript()
    helper.mockApp()
    #Create ssh connection
    conn = ssh.sshConnection(computer,user.ID,script)

    #Connect to computer
    err = conn.connect()

    #Test for no error
    if(err != pref.Success):
      return self.skipTest("Failed to connect to remote computer")


    err, id = conn.run()

    self.assertEqual(err, pref.Success)
    self.assertNotEqual(id, -1)

  def test_runScriptFileDNE(self):
    '''
    runs basic script
    '''
    

    #Create ssh connection
    conn = ssh.sshConnection(self.computer,self.user,self.script)

    #Connect to computer
    err = conn.connect()

    #Test for no error
    if(err != pref.Success):
      return self.skipTest("Failed to connect to remote computer")

    self.script.fileName = "sleepScript11.sh"

    err, id = conn.run()
    print(err)
    print("\n\n\n\n")
    self.assertEqual(err, pref.getError(pref.ERROR_FILE_NOT_FOUND))