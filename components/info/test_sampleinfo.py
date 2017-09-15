
import unittest
import pprint
import glob
from sampleinfo import SampleInfo, SampleBase, find_samples
from basedir import basedir
import networkx as nx

sheppy_1 = '{}/ee_to_ZH_Z_to_nunu_H_to_bb/ee_to_ZH_Z_to_nunu_Sep12_ZHnunubb_1b_A_6'.format(basedir('heppy'))
spythia_1 = '{}/ee_to_ZH_Z_to_nunu_Jun21_A_1'.format(basedir('pythia'))

class TestSampleInfo(unittest.TestCase):
    
    #----------------------------------------------------------------------
    def test_1(self):
        """info yaml file can be loaded"""
        sinfo = SampleInfo(sheppy_1)
        print sinfo
                
    def test_networkx(self):
        '''simple test of networkx on graph 1-2-3-4 5-6'''
        graph = nx.DiGraph()
        graph.add_edge(1, 2)
        graph.add_edge(2, 3)
        graph.add_edge(3, 4)
        graph.add_edge(5, 6)
        s1 = list(nx.dfs_preorder_nodes(graph, 2))
        self.assertEqual(s1, [2, 3, 4])
        
class TestSampleBase(unittest.TestCase) :
    """Test sample database software"""
    
    def test_1_find_samples(self):
        """Test that sample can be found properly in their base directory"""
        samples = find_samples(basedir())
        pprint.pprint(samples)
        for s in samples:
            yamls = glob.glob('/'.join([s, '*.yaml']))
            self.assertEqual(len(yamls), 1)
            
    def test_2_base_constructor(self):
        """Test that the sample base can be constructed.
        
        requires each sample to have a yaml file (where sample.name is defined)
        """
        sample_base = SampleBase(basedir())
      
      
########################################################################
class TestSampleBaseIntegrity(unittest.TestCase):
    """Test integrity of the sample database"""

    #----------------------------------------------------------------------
    def setUp(self):
        self.sb = SampleBase(basedir())
        
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
            descendants = self.sb.descendants(seed)
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
