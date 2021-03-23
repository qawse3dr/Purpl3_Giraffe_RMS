import libpurpl3.operations as ops
import libpurpl3.preferences as pref
import unittest

class blackListTesting(unittest.TestCase):
    def testNoFile(self):
        holder = ops.confirmValidCommads("poopLmao", {"oops", "I cant Do Math", "I have crippling depression"})
        self.assertEqual(pref.getError(pref.ERROR_FILE_NOT_FOUND), holder.Error)
    
    def testNoBlackListInFile(self):
        holder = ops.confirmValidCommads("blackListTestScript", {"pooooooop", "lmao", "depression"})
        self.assertEqual(holder, pref.Success)
    
    def testBlackListedCommandInFile(self):
        holder = ops.confirmValidCommads("blackListTestScript", {"pooooooop", "lmao", "depression"})
        self.assertEqual(holder.Error, pref.getError(pref.ERROR_BLACKLISTED_COMMAND))
    