import libpurpl3.preferences as pref
import libpurpl3.sshServer as ssh
import unittest



class BaseTestCase(unittest.TestCase):
  
  #Change to reflect your machine
  username = "root"
  ip = "localhost"

  #mock vars as db isn't complete yet
  computer = None 
  user = None
  script = None
  
  #reset the config before each test
  def setUp(self):
    pref.setConfigFile("tests/res/sshConfig.yaml")
    #values for mock object
    self.computer = type('Computer', (object,), 
      {
        'ip' : self.ip,
        'username': self.username
      })
    self.user = type('User', (object,), {'propertyName' : 'propertyValue'})
    self.script = type('Script', (object,), {'propertyName' : 'propertyValue'})
  
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

    self.computer.ip = "192.169.100.100"

    #Connect to computer
    err = conn.connect()

    #Test for no error
    self.assertEqual(err,pref.getError(pref.ERROR_CONNECTION_FAILED))



