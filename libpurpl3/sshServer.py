

import logging
import threading
import os
from typing import Tuple 
from flask import session
import datetime
import libpurpl3.preferences as pref 
import paramiko
import libpurpl3.tableOpComputer as computerTable
import libpurpl3.tableOpScript as scriptTable
import libpurpl3.tableOpScriptLog as scriptLogTable
import libpurpl3.tableOpUser as userTable
import libpurpl3.whitelistBlacklist as whitelistBlackList

#Creates logger
logger = logging.getLogger()

class sshConnection():
  '''
    Connection holding an ssh connection of a
    computer user and script.
    sshConnection(computer, user, script)
  '''

  computer = None
  script = None
  userID = None

  #ssh driver
  ssh = None
  def __init__(self, computer: computerTable.Computer, userID: int, script: scriptTable.Script):
    '''
      @param computer::Computer, is the computer connected though ssh
      @param userId::int the id of the currently logged in user
      @param script::Script, the script that is being run on the computer
    '''
    self.computer = computer
    self.script = script
    self.scriptLog = None
    self.userID = userID
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
      #make sure ip isnt Blacklisted
      blackListFileName = pref.getNoCheck(pref.CONFIG_BLACKLIST_IP_FILE)
      if(blackListFileName != ""):
        blackList = None
        try:
          blackList = [line.rstrip("\n") for line in open(blackListFileName)]
        except:
          tempErr = pref.getError(pref.ERROR_FILE_NOT_FOUND, args=(blackListFileName))
          logger.error(tempErr)
          break

        err = whitelistBlackList.confirmValidIP(self.computer.IP, blackList)
      else:
        logger.warning("no ip blacklist no filtering")

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
      #TODO test self.computer.IP, needs list of blacklisted commands
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

    ftp_client = None
    err = pref.Success

    for _ in range(1):

      #creates sftp connection
      try:
        ftp_client = self.ssh.open_sftp()
      except:
        err = pref.getError(pref.ERROR_UNKNOWN)
        break
      
      #Paths for scripts
      remoteFolder = pref.getNoCheck(pref.CONFIG_REMOTE_FOLDER)
      scriptFolder = pref.getNoCheck(pref.CONFIG_SCRIPT_PATH)

      #Checks whitelistBlackList
      for _ in range(1):
        blackListFileName = pref.getNoCheck(pref.CONFIG_BLACKLIST_CMD_FILE)
        if(blackListFileName != ""):
          blackList = None
          try:
            blackList = [line.rstrip("\n") for line in open(blackListFileName)]
          except:
            tempErr = pref.getError(pref.ERROR_FILE_NOT_FOUND, args=(blackListFileName))
            logger.error(tempErr)
            break

          err = whitelistBlackList.confirmValidCommads("{}{}".format(scriptFolder,self.script.fileName), blackList)
          if(err != pref.Success):
            logger.error(err)
            break
        else:
          logger.warning("no cmd blacklist no filtering")

      #Error during blacklist
      if err != pref.Success:
        logger.error(err)
        break

      #Copies script over
      err = copyFileToComputer(ftp_client, remoteFolder, scriptFolder, self.script.fileName)
      if(err != pref.Success):
        break
      
      #Executes script
 
      #windows echo command
      #echoCmd = "echo Returned $?"
      echoCmd = "printf \"\\n\nReturned: %d\" $?"
      _, stdout, stderr = self.ssh.exec_command("{}{}; {}".format(remoteFolder, self.script.fileName, echoCmd))

      #creates Script logs
      self.scriptLog = scriptLogTable.ScriptLogTable.createEntry(self.script.ID, self.userID, self.computer.ID, self.computer.asAdmin)
      err = scriptLogTable.ScriptLogTable.add(self.scriptLog)

      if(err == pref.Success):
        outputThread = threading.Thread(target=self.getOutput, daemon=True, args=(stdout,stderr))
        outputThread.start()

    
    id = self.scriptLog.ID if self.scriptLog != None else -1
    return err, id


  def getOutput(self, stdout: paramiko.ChannelFile, stderr : paramiko.ChannelFile):
    '''
    This should never be called from outside this class.
    And should be run in another thread retriving the output from the 
    script running on the remote computer
    it is assumed the scriptLog is already set before this function
    '''

    #sets it so chanels arent blocking
    stdout.channel.setblocking(0)
    stderr.channel.setblocking(0)

    stdout_buffer = ""
    stderr_buffer = ""

    #scriptLog folder
    logFolder = pref.getNoCheck(pref.CONFIG_SCRIPT_LOG_PATH)
    try:
      stdoutFile = open("{}{}".format(logFolder, self.scriptLog.stdoutFile),"w")
      stderrFile = open("{}{}".format(logFolder, self.scriptLog.stderrFile),"w")
    except: 
      #Couldn't create stdout and stderr file aborting and display warning
      err = pref.getError(pref.ERROR_CANT_CREATE_FILE, args=("{} and {}".format(self.scriptLog.stdoutFile, self.scriptLog.stderrFile)))
      logger.error(err)
      return
    #writes basic info to stdout and stderr
    stdoutFile.write("Script Start at: {}\n".format(datetime.datetime.now()))
    stderrFile.write("Script Start at: {}\n".format(datetime.datetime.now()))
    stdoutFile.write("{}: ".format(datetime.datetime.now()))
    stderrFile.write("{}: ".format(datetime.datetime.now()))
    stdoutFile.flush()
    stderrFile.flush()
    #gets the output
    while not stdout.channel.exit_status_ready() or not stderr.channel.exit_status_ready() or stdout.channel.recv_ready() or stderr.channel.recv_ready():
      #stdout
      
      if(stdout.channel.recv_ready()):
        try:
          stdout_buffer = stdout.read(1).decode()
          stdoutFile.write(stdout_buffer)
          if stdout_buffer == "\n":
            stdoutFile.write("{}: ".format(datetime.datetime.now()))
          stdoutFile.flush()
        except:
          pass
        
      #stderr
      if(stderr.channel.recv_ready()):
        try:
          stderr_buffer = stderr.read(1).decode()
          stderrFile.write(stderr_buffer)
          if stderr_buffer == "\n":
            stderrFile.write("{}: ".format(datetime.datetime.now()))
          stderrFile.flush()
        except:
          pass

    #writes rest of data
    for line in stdout.readlines():
      stdoutFile.write("{}: {}".format(datetime.datetime.now(),line))
    for line in stderr.readlines():
      stderrFile.write("{}: {}".format(datetime.datetime.now(),line))

    stdoutFile.close()
    stderrFile.close()

    #gets returnValue
    stdoutFile = open("{}{}".format(logFolder, self.scriptLog.stdoutFile), "r+")
    stdoutFile.seek(0,os.SEEK_END)
    end = stdoutFile.tell()
    buffer = ""
    counter = 1
    while( buffer != "\n"):
      stdoutFile.seek(end-counter,os.SEEK_SET)
      buffer = stdoutFile.read(1)
      counter += 1

    returnValue = stdoutFile.readline().split("Returned: ")
    
    err = pref.Success
    #Failed to get return value error reading connection losted
    if len(returnValue) == 1:
      err = pref.getError(pref.ERROR_SSH_CONNECTION_LOST,args=(self.computer.username,self.computer.IP,self.script.name))
      returnValue = None
      logger.error(err)
    else:
      returnValue = returnValue[-1]
      logger.info("Complete script {} with return value {}".format(self.script.name, returnValue))
    self.scriptLog.endTime = datetime.datetime.now()
    self.scriptLog.errorCode = err.code
    self.scriptLog.returnVal = returnValue
    self.ssh.close()

    #Writes return value to db
    scriptLogTable.ScriptLogTable.editEntry(self.scriptLog)
    
  @staticmethod
  def addNewComputer(computerIP: str,username: str, password:str) -> pref.Error:
    '''
    adds a new computer with using its username and password
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
      #make sure ip isnt Blacklisted
      blackListFileName = pref.getNoCheck(pref.CONFIG_BLACKLIST_IP_FILE)
      if(blackListFileName != ""):
        blackList = None
        try:
          blackList = [line.rstrip("\n") for line in open(blackListFileName)]
        except:
          tempErr = pref.getError(pref.ERROR_FILE_NOT_FOUND, args=(blackListFileName))
          logger.error(tempErr)
          break

        err = whitelistBlackList.confirmValidIP(computerIP, blackList)
        if(err != pref.Success):
          logger.error(err)
          break
      else:
        logger.warning("no ip blacklist no filtering")

      #get shh public key
      sshKey = pref.getNoCheck(pref.CONFIG_PUBLIC_SSH_KEY)

      #if its empty row public sshkey empty
      if(sshKey == None or sshKey.strip().strip("\n") == ""):
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

    return err

  def __str__(self):
    return "sshSever run on {}@{} by executed by {}, to run script {}".format(self.computer.username,self.computer.ip,self.userID,self.script.name) 


def copyFileToComputer(ftp_client: paramiko.SFTPClient, remoteFolder: str,resFolder: str, filename: str) -> pref.Error:
  '''
  Copies a file to a remote computer ftp_client
  @param ftp_client:parmiko.STFPClient the ssh ftp connection what the file will be transferred over
  @param remoteFolder:str 
  '''
  err = pref.Success

  #creates folder if it doesn't exist
  try:
    ftp_client.mkdir(remoteFolder, mode=0o777)
  except: #This is happen if the folder already exists .
    pass

  #copies file
  try:
    ftp_client.put("{}{}".format(resFolder,filename),"{}{}".format(remoteFolder,filename))
    ftp_client.chmod("{}{}".format(remoteFolder,filename), 0o777)
  except Exception as e:
    print(e)
    #couldn't find script on sever.
    err = pref.getError(pref.ERROR_FILE_NOT_FOUND, args=(resFolder+filename))
    logger.error(err)
  
  if(ftp_client):
    ftp_client.close()
  return err

