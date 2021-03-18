

import logging
import libpurpl3.preferences as pref 
import paramiko

#Creates logger
logger = logging.getLogger("purpl3_rms")

class sshConnection():
  '''
    Connection holding an ssh connection of a
    computer user and script.
    sshConnection(computer, user, script)
  '''

  #TODO change to computer class
  computer = None

  #TODO change to user class
  user = None

  #TODO change to script class
  script = None

  #ssh driver
  ssh = None
  def __init__(self, computer, user, script):
    '''
      @param computer::Computer, is the computer connected though ssh
      @param user::User, the user that started the script (not the user logged into the computer)
      @param script::Script, the script that is being run on the computer
    '''
    self.computer = computer
    self.user = user
    self.script = script

  def connect(self) -> pref.Error:
    
    err = pref.Success

    for _ in range(1):
      #Create ssh client with basic autoadd settings
      self.ssh = paramiko.SSHClient()
      self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

      #Get Keyfile from preferences
      try:
        keyFileName = pref.getNoCheck(pref.CONFIG_PRIVATE_SSH_KEY)
        keyFile = paramiko.RSAKey.from_private_key_file(keyFileName)
      except:
        err = pref.getError(pref.ERROR_CANT_FIND_SSH_KEY,args=(keyFileName))
        logger.error(err)
        break
      
      #connect to the computer
      try:        
        self.ssh.connect(self.computer.ip, username=self.computer.username, pkey = keyFile, timeout=5)

      except paramiko.ssh_exception.AuthenticationException as e:
        err = pref.getError(pref.ERROR_SSH_AUTHENTICATION_FAILED,args=(self.computer.username,self.computer.ip))
        logger.error(err)
        break
      except:
        err = pref.getError(pref.ERROR_CONNECTION_FAILED,args=(self.computer.username,self.computer.ip))
        logger.error(err)

    return err


  def run(self) -> pref.Error:
    return pref.Success

  @staticmethod
  def addNewComputer(username: str, password:str):
    #ftp_client = ssh.open_sftp()
    #try:
    #  ftp_client.mkdir("/tmp/Purpl3_RMS")
    #except:
    #  pass
    #ftp_client.put("addSSHKey.sh","/tmp/Purpl3_RMS/addSSHKey.sh")
    #ftp_client.chmod("/tmp/Purpl3_RMS/addSSHKey.sh", 0o777)
    #stdin, stdout, stderr =  ssh.exec_command("/tmp/Purpl3_RMS/addSSHKey.sh")
    pass


  def __str__(self):
    return "" 


