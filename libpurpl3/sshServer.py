

import logging
from typing import Tuple 
import datetime
import libpurpl3.preferences as pref 
import paramiko
import libpurpl3.tableOpComputer as computerTable
import libpurpl3.tableOpScript as scriptTable
import libpurpl3.tableOpUser as userTable

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
  def __init__(self, computer: computerTable.Computer, user: userTable.User, script: scriptTable.Script):
    '''
      @param computer::Computer, is the computer connected though ssh
      @param user::User, the user that started the script (not the user logged into the computer)
      @param script::Script, the script that is being run on the computer
    '''
    self.computer = computer
    self.user = user
    self.script = script
    self.scriptLog = None
  def connect(self) -> pref.Error:
    '''
    Connects its self to the computer based on
    the computer object passed in init.
    The computer with its IP and username.
    Before a computer can be connected to for the
    first time addComputer must first be run on it.
    @returns the error code pref.Success if it worked
    '''

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
        self.ssh.connect(self.computer.IP, username=self.computer.username, pkey = keyFile, timeout=5, allow_agent=False)
      #Authentication error rerun addComputer on this computer to fix
      except paramiko.ssh_exception.AuthenticationException as e:
        err = pref.getError(pref.ERROR_SSH_AUTHENTICATION_FAILED,args=(self.computer.username,self.computer.IP))
        logger.error(err)
        break
      #Failed to connect
      except:
        err = pref.getError(pref.ERROR_CONNECTION_FAILED,args=(self.computer.username,self.computer.IP))
        logger.error(err)

    return err


  def run(self) -> Tuple[pref.Error, int]:
    ''' Runs a script based on the script passed in init'''
    err = pref.Success
    return err, 0


  def getOutput(self):
    '''
    This should never be called from outside this class.
    And should be run in another thread retriving the output from the 
    script running on the remote computer
    it is assumed the scriptLog is already set before this function
    '''
    err = pref.Success

  @staticmethod
  def addNewComputer(computerIP: str,username: str, password:str, userID: int = None, name:str = None, nickName:str =None , desc:str = None, asAdmin:bool = False) -> pref.Error:
    '''
    adds a new computer with using its username and password
    and adds it to the db.
    @param computerIP:str ip of the computer to add as a string.
    @param username:str username of the computer not user adding the computer.
    @param password:str password of the user described above.
    @return err
    '''
    
    #init values
    err = pref.Success
    ssh = None
    ftp_client = None
    remoteFolder = None
    stdin = None
    stdout = None
    stderr = None

    for _ in range(1):
      #get shh public key
      sshKey = pref.getNoCheck(pref.CONFIG_PUBLIC_SSH_KEY)

      #if its empty row public sshkey empty
      if(sshKey == ""):
        err = pref.getError(pref.ERROR_EMPTY_SSH_PUBLIC_KEY)
        logger.error(err)
        break
    
      #Create ssh client with basic autoadd settings
      ssh = paramiko.SSHClient()
      ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
      
      #Connects to computer with password and username
      try:
        ssh.connect(computerIP, username=username, password = password, timeout=5, look_for_keys=False, allow_agent=False)
        ftp_client = ssh.open_sftp()
      #Incorrect username or password
      except paramiko.ssh_exception.AuthenticationException as e:
        err = pref.getError(pref.ERROR_SSH_AUTHENTICATION_FAILED,args=(username,computerIP))
        logger.error(err)
        break
      #Connection timed out or port rejected.
      except:
        err = pref.getError(pref.ERROR_CONNECTION_FAILED,args=(username,computerIP))
        logger.error(err)
        break

      #Create tempfolder on the remote computer.
      remoteFolder = pref.getNoCheck(pref.CONFIG_REMOTE_FOLDER)
      addSSHKeyScript = pref.getNoCheck(pref.CONFIG_ADD_COMPUTER_SCRIPT)
      resFolder = pref.getNoCheck(pref.CONFIG_RES_FOLDER)

      #Add ssh file to server and change permissions.
      err = copyFileToComputer(ftp_client,remoteFolder,resFolder,addSSHKeyScript)
      if(err != pref.Success):
        break

      #Run setup script with sshKey config file.
      try:
        stdin, stdout, stderr =  ssh.exec_command("sshkey=\"{}\" {}{} > /dev/null; echo $?".format(sshKey,remoteFolder,addSSHKeyScript))
      except:
        #failed to execute script.
        err = pref.getError(pref.ERROR_SSH_FAILED_TO_EXECUTE_SCRIPT, args=(addSSHKeyScript))
        logger.error(err)
        break
      
      #Check error code of script.
      errCode = "".join(stdout.readlines()).rstrip("\n")
      if(errCode != "0"):
        err = pref.getError(pref.ERROR_SSH_SCRIPT_FAILED_WITH_ERROR_CODE,args=(errCode))
        logger.error(err)

    #Adds computer to db
    if(err == pref.Success):
      #TODO change to now way of creating computer when updated
      computer = computerTable.Computer(None,userID,name,nickName,desc,username,computerIP,datetime.datetime.now(),datetime.datetime.now(),asAdmin)
      computerTable.ComputerTable.add(computer)
    return err

  def __str__(self):
    return "sshSever run on {}@{} by executed by {}, to run script {}".format(self.computer.username,self.computer.ip,self.user.name,self.script.name) 


def copyFileToComputer(ftp_client: paramiko.SFTPClient, remoteFolder: str,resFolder: str, filename: str) -> pref.Error:
  '''
  Copies a file to a remote computer ftp_client
  @param ftp_client:parmiko.STFPClient the ssh ftp connection what the file will be transferred over
  @param remoteFolder:str 
  '''
  err = pref.Success

  #creates folder if it doesn't exist
  try:
    ftp_client.mkdir(remoteFolder)
  except: #This is happen if the folder already exists .
    pass

  #copies file
  try:
    ftp_client.put("{}{}".format(resFolder,filename),"{}{}".format(remoteFolder,filename))
    ftp_client.chmod("{}{}".format(remoteFolder,filename), 0o777)
  except paramiko.SFTP_NO_SUCH_FILE:
    #couldn't find script on sever.
    err = pref.getError(pref.ERROR_FILE_NOT_FOUND, args=(resFolder+filename))
    logger.error(err)
  except paramiko.SFTP_PERMISSION_DENIED:
    #permission denied.
    err = pref.getError(pref.ERROR_SSH_PERMISSION_DENIED, args=(remoteFolder))
    logger.error(err)
  except Exception as e:
    #Unknown error.
    err = pref.getError(pref.ERROR_UNKNOWN, args=(e))
    logger.error(err)
  return err

