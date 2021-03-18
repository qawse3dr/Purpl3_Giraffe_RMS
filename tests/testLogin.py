import unittest
import libpurpl3.login as login
from libpurpl3.tableOpUser import *
from flask import jsonify
from unittest.mock import MagicMock

loginHolder = UserTable()
loginHolder.checkLogin = MagicMock(return_value=False)     

if __name__ == '__main__':
    unittest.main()
