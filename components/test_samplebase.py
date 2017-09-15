
import unittest
import pprint
import glob

from samplebase import SampleBase, find_samples, basedir

class TestSampleBase(unittest.TestCase) :

    def test_1_find_samples(self):
        samples = find_samples(basedir)
        pprint.pprint(samples)
        for s in samples:
            yamls = glob.glob('/'.join([s, '*.yaml']))
            self.assertEqual(len(yamls), 1)
            
    def test_2_base_constructor(self):
        sample_base = SampleBase(basedir)
        
    
        
if __name__ == '__main__':
    unittest.main()
    
