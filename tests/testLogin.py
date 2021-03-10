import unittest
import libpurpl3.login as login
from flask import jsonify
from cryptography.fernet import Fernet

class BaseTestCase(unittest.TestCase):
    def testPasswordEncryption(self):
        key = Fernet.generate_key()
        cipher_suite = Fernet(key)
        holder = cipher_suite.encrypt("THIS_1S-P0ggers".encode())
        holder2 = login.encryptPassword("THIS_1S-P0ggers", key)
        self.assertEqual(holder, holder2)
    
    def testPasswordDecryption(self):
        key = Fernet.generate_key()
        cipher_suite = Fernet(key)
        holder = login.encryptPassword("THIS_1S-P0ggers", key)
        self.assertEqual("THIS_1S-P0ggers".encode(), cipher_suite.decrypt(holder))
        

    




        
    

if __name__ == '__main__':
    unittest.main()
