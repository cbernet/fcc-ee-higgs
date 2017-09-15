import unittest

from FCCComponent import FCCComponent
from basedir import basedir

class Test_FCCComponent(unittest.TestCase):
    
    def test_1(self):
        comp = FCCComponent('{}/ee_to_ZH_Z_to_nunu_H_to_bb/ee_to_ZH_Z_to_nunu_Sep12_ZHnunubb_1b_A_6'.format(basedir('heppy')))
        self.assertTrue(True)
    
if __name__ == "__main__":
    
    unittest.main()
