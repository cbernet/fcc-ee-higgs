
import unittest
from sampleinfo import SampleInfo, SampleInfoGraph
from fcc_ee_higgs.components.basedir import basedir
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
        
    def test_mother(self):
        heppy_info = SampleInfo(sheppy_1)
        pythia_info = SampleInfo(spythia_1)
        samples = SampleInfoGraph([heppy_info, pythia_info])
        self.assertEqual(samples.oldest_ancestor(heppy_info), pythia_info)
        
        
if __name__ == '__main__':
    unittest.main()
