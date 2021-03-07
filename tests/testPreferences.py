import libpurpl3.preferences as pref
import unittest

class BaseTestCase(unittest.TestCase):
    #reset the config before each test
    def setUp(self):
      pref.resetConfig()

    #Tests simple case with a valid config
    def test_setConfigFile(self):
      err = pref.setConfigFile("tests/res/test1Conf.yaml")
      self.assertEqual(err,pref.Success)
    
    #Tests complex case with a valid config
    def test_setConfigFileComplex(self):
      err = pref.setConfigFile("tests/res/test2Conf.yaml")
      self.assertEqual(err.code,pref.Success.code)

      self.assertEqual("null",pref.getError(pref.ERROR_UNKNOWN))

      self.assertEqual("/test", pref.getNoCheck(pref.CONFIG_LOGIN_ENDPOINT))
    #Tests simple case with a file that doesn't exist
    def test_setConfigFileDNE(self):
      err = pref.setConfigFile("tests/res/DOESNOTEXIST")
      self.assertEqual(err.code,pref.getNoCheck(pref.ERROR_FILE_NOT_FOUND).code)
    
    #Tests simple case with a file that doesn't exist
    def test_setConfigFileInvalidFile(self):
      err = pref.setConfigFile("tests/res/badConf.yaml")
      self.assertEqual(err.code,pref.getNoCheck(pref.ERROR_ATTRIBUTE_NOT_FOUND).code)
    
    #Tests pref.get default value
    def test_get(self):
      err,login = pref.get(pref.CONFIG_LOGIN_ENDPOINT)
      self.assertEqual("/login",login)
      self.assertEqual(pref.Success.code,err.code)
    
    #Tests pref.get invalid key
    def test_getInvalidKey(self):
      err,dne = pref.get("DNE")
      self.assertEqual(None,dne)
      self.assertEqual(pref.getError(pref.ERROR_ATTRIBUTE_NOT_FOUND).code,err.code)
    
    #Tests pref.getNoCheck default value
    def test_getNoCheck(self):
      login = pref.getNoCheck(pref.CONFIG_LOGIN_ENDPOINT)
      self.assertEqual("/login",login)

    #Tests pref.getNoCheck invalid key
    def test_getNoCheckInvalidKey(self):
      err,dne = pref.get("DNE")
      self.assertEqual(None,dne)
         
    #Tests pref.setAttr with a valid key 
    def test_setAttr(self):
      err = pref.setAttr(pref.CONFIG_LOGIN_ENDPOINT, "/login2")
      self.assertEqual(pref.Success.code,err.code)

      err, login = pref.get(pref.CONFIG_LOGIN_ENDPOINT)
      self.assertEqual("/login2",login)
      self.assertEqual(pref.Success.code,err.code)
    
    #Tests pref.setAttr with a valid key for a key instead a dict 
    def test_setAttrInDict(self):
      err = pref.setAttr(pref.ERROR_UNKNOWN, "error")
      self.assertEqual(pref.Success.code,err.code)

      err, unknownErr = pref.get(pref.ERROR_UNKNOWN)
      self.assertEqual("error",unknownErr)
      self.assertEqual(pref.Success.code,err.code)
    
    #Tests test reset 
    def test_setAttrAndReset(self):

      #check that the value is correct to start
      err, unknownErr = pref.get(pref.ERROR_UNKNOWN)
      self.assertEqual(pref.getError(pref.ERROR_UNKNOWN).code,unknownErr.code)
      self.assertEqual(pref.Success.code,err.code)

      #set new value
      err = pref.setAttr(pref.ERROR_UNKNOWN, "error")
      self.assertEqual(pref.Success.code,err.code)
      
      #check new value
      err, unknownErr = pref.get(pref.ERROR_UNKNOWN)
      self.assertEqual("error",unknownErr)
      self.assertEqual(pref.Success.code,err.code)

      #reset config
      pref.resetConfig()

      #check that the value was reset
      err, unknownErr = pref.get(pref.ERROR_UNKNOWN)
      self.assertEqual(pref.getError(pref.ERROR_UNKNOWN).code,unknownErr.code)
      self.assertEqual(pref.Success.code,err.code)


        
    

if __name__ == '__main__':
    unittest.main()
