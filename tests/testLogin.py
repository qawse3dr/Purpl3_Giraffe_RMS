from flask import jsonify
from cryptography.fernet import Fernet
import unittest
import libpurpl3.login as login

class BaseTestCase(unittest.TestCase):
    def testPasswordEncryption(self):
        key = Fernet.generate_key()
        cipher_suite = Fernet(key)
        holder = cipher_suite.encrypt("THIS_1S-P0ggers".encode())
        holder2 = login.encryptPassword("THIS_1S-P0ggers", key)
        self.assertEqual(holder, holder2)




        
    

if __name__ == '__main__':
    unittest.main()
