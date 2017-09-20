import unittest
from fcc_ee_higgs.components.all import load_components

class TestAll(unittest.TestCase):
    
    def test_heppy(self):
        components = load_components(mode='heppy')
        
    def test_pythia(self):
        components = load_components(mode='pythia')
        
if __name__ == "__main__":
    unittest.main()
        
