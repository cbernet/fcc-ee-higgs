
import unittest
import pprint
import glob

from samplebase import SampleBase, find_samples, basedir

class TestSampleBase(unittest.TestCase) :
    """Test sample database software"""
    
    def test_1_find_samples(self):
        """Test that sample can be found properly in their base directory"""
        samples = find_samples(basedir)
        pprint.pprint(samples)
        for s in samples:
            yamls = glob.glob('/'.join([s, '*.yaml']))
            self.assertEqual(len(yamls), 1)
            
    def test_2_base_constructor(self):
        """Test that the sample base can be constructed.
        
        requires each sample to have a yaml file (where sample.name is defined)
        """
        sample_base = SampleBase(basedir)
      
      
########################################################################
class TestSampleBaseIntegrity(unittest.TestCase):
    """Test integrity of the sample database"""

    #----------------------------------------------------------------------
    def setUp(self):
        self.sb = SampleBase(basedir)
        
    def test_id_unique(self):
        '''Test that sample ids are indeed unique'''
        ids = [sinfo.id for sinfo in self.sb.values()]
        self.assertEqual(len(set(ids)), len(ids))
        
    def test_njobs(self):
        '''Test that njobs_ok is equal or smaller than njobs'''
        for sinfo in self.sb.values():
            self.assertGreaterEqual(sinfo['sample']['njobs'], sinfo['sample']['njobs_ok'])
        
    def test_hierarchy(self):
        '''test that in a family, cross section is the same, and nevents decreases'''
        # select samples with no mother:
        seeds = [sinfo for sinfo in self.sb.values() if
                 len(sinfo.mothers()) == 0]
        for seed in seeds:
            descendants = self.sb.graph.descendants(seed)
            xsec = None
            nevents = seed['sample']['nevents']
            for sinfo in descendants:
                if xsec is None:
                    xsec = sinfo['sample']['xsection']
                else:
                    self.assertEqual(sinfo['sample']['xsection'], xsec)
                self.assertGreaterEqual(nevents, sinfo['sample']['nevents'])
                nevents = sinfo['sample']['nevents']
    
    
    
    
        
if __name__ == '__main__':
    unittest.main()
    
