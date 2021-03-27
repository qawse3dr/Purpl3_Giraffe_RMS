import libpurpl3.whitelistBlacklist as blacklist 
import libpurpl3.preferences as pref
import unittest

class blackListTesting(unittest.TestCase):
    def testNoFile(self):
        holder = blacklist.confirmValidCommads("poopLmao", ["oops", "I cant Do Math", "I have crippling depression"])
        self.assertEqual(pref.getError(pref.ERROR_FILE_NOT_FOUND), holder)
    
    def testNoBlackListInFile(self):
        holder = blacklist.confirmValidCommads("tests/res/blackListTestScript", ["pooooooop", "lmao", "depression"])
        self.assertEqual(holder, pref.Success)
    
    def testBlackListedCommandInFile(self):
        holder = blacklist.confirmValidCommads("tests/res/blackListTestScript", ["pooooooop", "lmao", "delete"])
        self.assertEqual(holder, pref.getError(pref.ERROR_BLACKLISTED_COMMAND))
    