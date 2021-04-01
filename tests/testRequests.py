import libpurpl3.preferences as pref
import libpurpl3.sshServer as ssh
import libpurpl3.tableOpComputer as computerTable
import libpurpl3.tableOpScript as ScriptTable
from Purpl3_RMS import app
import datetime
import unittest
import tests.testHelpers as helper
from flask import session


class BaseTestCase(unittest.TestCase):
  
  user = None
  script = None
  computer = None
  c = None
  def setUp(self):
    helper.clearDB()
    helper.createMockDB()
    self.user = helper.createUserAccount()
    self.script = helper.createScript()
    self.computer = helper.createComputer()
    self.c = helper.mockApp()
    
  def test_ping(self):
    '''
    Tests ping endpoint
    '''

    rv = self.c.post('/ping')
    
    expected = {
      "ping": "pong"
    }
    self.assertEqual(rv.get_json(),expected)

  def test_api_runScript(self):
    '''
    Tests runScript from and endpoint perpective
    '''
    params = {
      pref.getNoCheck(pref.REQ_VAR_BODY):{
        pref.getNoCheck(pref.REQ_VAR_OP): pref.getNoCheck(pref.OPERATION_RUN_SCRIPT),
        pref.getNoCheck(pref.REQ_VAR_DATA):{
          pref.getNoCheck(pref.REQ_VAR_SCRIPT_ID): 1,
          pref.getNoCheck(pref.REQ_VAR_COMPUTER_ID): 1,
        }
      }
      
    }
    rv = self.c.post('/api', json=params)

    expected = {
      "Error": pref.Success.toJson(),
      "Id": 1
    }
    print(rv.get_json())
    self.assertEqual(rv.get_json(), expected)
  def test_api_getall_scripts(self):
    '''
    Tests get all for scripts
    '''
    params = {
      pref.getNoCheck(pref.REQ_VAR_BODY):{
        pref.getNoCheck(pref.REQ_VAR_OP): pref.getAttrName(pref.getNoCheck(pref.OPERATION_MANAGE_SCRIPT)),
        pref.getNoCheck(pref.REQ_VAR_DATA):{
          pref.getNoCheck(pref.REQ_VAR_FUNC_OP): pref.getNoCheck(pref.TABLE_OP_GET_ALL),
          pref.getNoCheck(pref.REQ_VAR_DATA):{
          }
        }
      }
      
    }
    rv = self.c.post('/api', json=params)

    self.assertEqual(rv.get_json()["Error"]["code"],0)

  def test_api_getall_computer(self):
    '''
    Tests getall for computers
    '''
    params = {
      pref.getNoCheck(pref.REQ_VAR_BODY):{
        pref.getNoCheck(pref.REQ_VAR_OP): pref.getAttrName(pref.getNoCheck(pref.OPERATION_MANAGE_COMPUTERS)),
        pref.getNoCheck(pref.REQ_VAR_DATA):{
          pref.getNoCheck(pref.REQ_VAR_FUNC_OP): pref.getNoCheck(pref.TABLE_OP_GET_ALL),
          pref.getNoCheck(pref.REQ_VAR_DATA):{
          }
        }
      }
      
    }
    rv = self.c.post('/api', json=params)
    self.assertEqual(rv.get_json()["Error"]["code"],0)

  def test_api_getall_scriptLogs(self):
    '''
    Tests get all for scriptLogs
    '''
    params = {
      pref.getNoCheck(pref.REQ_VAR_BODY):{
        pref.getNoCheck(pref.REQ_VAR_OP): pref.getAttrName(pref.getNoCheck(pref.OPERATION_MANAGE_SCRIPT_LOGS)),
        pref.getNoCheck(pref.REQ_VAR_DATA):{
          pref.getNoCheck(pref.REQ_VAR_FUNC_OP): pref.getNoCheck(pref.TABLE_OP_GET_ALL),
          pref.getNoCheck(pref.REQ_VAR_DATA):{
          }
        }
      }
      
    }
    rv = self.c.post('/api', json=params)
    self.assertEqual(rv.get_json()["Error"]["code"],0)

  def test_api_add_computer_invalidPassword(self):
    '''
    tests add computer from request with an invalid password
    '''
    pref.setAttr(pref.CONFIG_PUBLIC_SSH_KEY,"dafsdfas")
    
    params = {
      pref.getNoCheck(pref.REQ_VAR_BODY):{
        pref.getNoCheck(pref.REQ_VAR_OP): pref.getAttrName(pref.getNoCheck(pref.OPERATION_MANAGE_COMPUTERS)),
        pref.getNoCheck(pref.REQ_VAR_DATA):{
          pref.getNoCheck(pref.REQ_VAR_FUNC_OP): pref.getNoCheck(pref.TABLE_OP_ADD),
          pref.getNoCheck(pref.REQ_VAR_DATA):{
            pref.getNoCheck(pref.REQ_VAR_NICK_NAME): "Larry's Computer",
            pref.getNoCheck(pref.REQ_VAR_DESC): "ITS MAH COMPUTER",
            pref.getNoCheck(pref.REQ_VAR_USERNAME): "root",
            pref.getNoCheck(pref.REQ_VAR_PASSWORD): "NOT MY PASSWORD",
            pref.getNoCheck(pref.REQ_VAR_IP): "localhost",
            pref.getNoCheck(pref.REQ_VAR_IS_ADMIN): False
          }
        }
      }
      
    }
    rv = self.c.post('/api', json=params)
    self.assertEqual(rv.get_json()["Error"]["code"],50)


  def test_api_add_script(self):
    '''
    Tests add script function for the script larryScript.sh
    it will delete the file if it exists before the tests
    '''
    import os

    #remove test file incase it already there
    try:
      scriptLocation = pref.getNoCheck(pref.CONFIG_SCRIPT_PATH)
      os.remove("{}{}".format(scriptLocation,"larryScript.sh"))
    except:
      pass
    params = {
      pref.getNoCheck(pref.REQ_VAR_BODY):{
        pref.getNoCheck(pref.REQ_VAR_OP): pref.getAttrName(pref.getNoCheck(pref.OPERATION_MANAGE_SCRIPT)),
        pref.getNoCheck(pref.REQ_VAR_DATA):{
          pref.getNoCheck(pref.REQ_VAR_FUNC_OP): pref.getNoCheck(pref.TABLE_OP_ADD),
          pref.getNoCheck(pref.REQ_VAR_DATA):{
            pref.getNoCheck(pref.REQ_VAR_NICK_NAME): "Larry's SCRIPT",
            pref.getNoCheck(pref.REQ_VAR_DESC): "LARRY's SCRIPTS",
            pref.getNoCheck(pref.REQ_VAR_FILE_NAME): "larryScript.sh",
            pref.getNoCheck(pref.REQ_VAR_SCRIPT_DATA): "NOT MY data",
            pref.getNoCheck(pref.REQ_VAR_IS_ADMIN): False
          }
        }
      }
      
    }
    rv = self.c.post('/api', json=params)
    self.assertEqual(rv.get_json()["Error"]["code"],0)


  def test_api_get_file_script(self):
    '''
    Tests getScript function with sleep script testing correct entry data
    and correct errorCode
    '''


    params = {
      pref.getNoCheck(pref.REQ_VAR_BODY):{
        pref.getNoCheck(pref.REQ_VAR_OP): pref.getAttrName(pref.getNoCheck(pref.OPERATION_MANAGE_SCRIPT)),
        pref.getNoCheck(pref.REQ_VAR_DATA):{
          pref.getNoCheck(pref.REQ_VAR_FUNC_OP): pref.getNoCheck(pref.TABLE_OP_GET_FILE),
          pref.getNoCheck(pref.REQ_VAR_DATA):{
            pref.getNoCheck(pref.REQ_VAR_ID): 1,
            pref.getNoCheck(pref.REQ_VAR_FILE_TYPE): pref.getNoCheck(pref.REQ_VAR_FILE_SCRIPT),
            pref.getNoCheck(pref.REQ_VAR_FP): 0 ,
          }
        }
      }
      
    }
    fileString = "#!/bin/bash\n\necho \"Program starts\"\necho \"waits 10 seconds\"\nsleep 10\necho \"waited 10 seconds wait 1 more\"\nsleep 1\necho \"exiting\"\n"
    rv = self.c.post('/api', json=params)
    self.assertEqual(rv.get_json()["Error"]["code"],0)
    self.assertEqual(rv.get_json()["entry"],fileString)

  def test_login_request_success(self):
    '''
    Tests a login request with a valid login
    '''

    params = {
      pref.getNoCheck(pref.REQ_VAR_BODY):{
        pref.getNoCheck(pref.REQ_VAR_OP): pref.getAttrName(pref.getNoCheck(pref.LOGIN_LOGIN)),
        pref.getNoCheck(pref.REQ_VAR_DATA):{
          pref.getNoCheck(pref.LOGIN_USERNAME): "unittest",
          pref.getNoCheck(pref.LOGIN_PASSWORD): "unittest"
        }
      }
    }

    rv = self.c.post('/login', json=params)
    self.assertEqual(rv.get_json()["Error"]["code"],0)

  def test_login_request_fail(self):
    '''
    Tests a login request with a invalid login due to invalid password
    '''

    params = {
      pref.getNoCheck(pref.REQ_VAR_BODY):{
        pref.getNoCheck(pref.REQ_VAR_OP): pref.getAttrName(pref.getNoCheck(pref.LOGIN_LOGIN)),
        pref.getNoCheck(pref.REQ_VAR_DATA):{
          pref.getNoCheck(pref.LOGIN_USERNAME): "unittest",
          pref.getNoCheck(pref.LOGIN_PASSWORD): "IncorrectPassword"
        }
      }
    }


    rv = self.c.post('/login', json=params)
    self.assertEqual(rv.get_json()["Error"]["code"],pref.getError(pref.ERROR_USER_AUTHENTICATION_ERROR).code)

  def test_get_by_ID(self):
    '''
    Tests get by id for an object that exists
    '''
    params = {
      pref.getNoCheck(pref.REQ_VAR_BODY):{
        pref.getNoCheck(pref.REQ_VAR_OP): pref.getAttrName(pref.getNoCheck(pref.OPERATION_MANAGE_SCRIPT)),
        pref.getNoCheck(pref.REQ_VAR_DATA):{
          pref.getNoCheck(pref.REQ_VAR_FUNC_OP): pref.getNoCheck(pref.TABLE_OP_GET_BY_ID),
          pref.getNoCheck(pref.REQ_VAR_DATA):{
            pref.getNoCheck(pref.REQ_VAR_ID): 1,
          }
        }
      }
    }

    rv = self.c.post("/api", json=params)
    
    self.assertEqual(rv.get_json()["Error"]["code"],0)
    self.assertEqual(rv.get_json()["entry"]["ID"],'1')

  def test_get_by_ID_DNE(self):
    '''
    Tests get by id for an object that doesnt exist
    '''
    params = {
      pref.getNoCheck(pref.REQ_VAR_BODY):{
        pref.getNoCheck(pref.REQ_VAR_OP): pref.getAttrName(pref.getNoCheck(pref.OPERATION_MANAGE_SCRIPT)),
        pref.getNoCheck(pref.REQ_VAR_DATA):{
          pref.getNoCheck(pref.REQ_VAR_FUNC_OP): pref.getNoCheck(pref.TABLE_OP_GET_BY_ID),
          pref.getNoCheck(pref.REQ_VAR_DATA):{
            pref.getNoCheck(pref.REQ_VAR_ID): 99,
          }
        }
      }
    }

    rv = self.c.post("/api", json=params)
    
    self.assertEqual(rv.get_json()["Error"]["code"],pref.getError(pref.ERROR_SQL_RETURN_MISSING_ATTR).code)

  def test_logout(self):

    paramsLogin = {
      pref.getNoCheck(pref.REQ_VAR_BODY):{
        pref.getNoCheck(pref.REQ_VAR_OP): pref.getAttrName(pref.getNoCheck(pref.LOGIN_LOGIN)),
        pref.getNoCheck(pref.REQ_VAR_DATA):{
          pref.getNoCheck(pref.LOGIN_USERNAME): "unittest",
          pref.getNoCheck(pref.LOGIN_PASSWORD): "unittest"
        }
      }
    }

    paramsLogout = {
      pref.getNoCheck(pref.REQ_VAR_BODY):{
        pref.getNoCheck(pref.REQ_VAR_OP): pref.getAttrName(pref.getNoCheck(pref.LOGIN_LOGOUT)),
        pref.getNoCheck(pref.REQ_VAR_DATA):{
        }
      }
    }

    with self.c as cLogin:
      rv = cLogin.post('/login', json=paramsLogin)
      self.assertEqual(True, pref.getNoCheck(pref.REQ_VAR_USER_ID) in session)
      rv = cLogin.post('/login', json=paramsLogout)
      self.assertEqual(rv.get_json()["Error"]["code"],0)
      self.assertEqual(False, pref.getNoCheck(pref.REQ_VAR_USER_ID) in session)
