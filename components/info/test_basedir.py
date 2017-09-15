import unittest

from basedir import basedir

class TestBaseDir(unittest.TestCase):
    
    def test_notier_exist(self):
        '''test that the base sample directory exists on this machine'''
        base = basedir()
        base = basedir('heppy')
        base = basedir('pythia')        
        self.assertTrue(True)
        
    def test_badtier(self):
        with self.assertRaises(ValueError) as err:
            basedir('blah')
