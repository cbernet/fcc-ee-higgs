import unittest
from collections import OrderedDict

from fcc_ee_higgs.plot.cuts import Cuts

class TestCuts(unittest.TestCase):
    
    def setUp(self):
        self.cuts = Cuts([
            ('cut3', '300'),
            ('cut1', '100'), 
            ('cut2', '200')
        ])
 
        
    def test_odict(self):
        '''Test the OrderedDict class to make sure it is suitable to be used for Cuts'''
        d = OrderedDict([
            ('b', 1), 
            ('a', 2),
            ('c', 3)
        ])
        self.assertListEqual(d.values(), [1, 2, 3])
        self.assertListEqual(d.keys(), ['b', 'a', 'c'])
        self.assertEqual(d['c'], 3)
        d.pop('a')
        self.assertListEqual(d.keys(), ['b', 'c'])
        self.assertListEqual(d.values(), [1, 3])
    
    def test_cuts(self):
        self.assertEqual(str(self.cuts), '300 && 100 && 200')
        self.cuts.pop('cut1')
        self.assertEqual(str(self.cuts), '300 && 200')
        self.cuts['cut4'] = '400'
        self.assertEqual(str(self.cuts), '300 && 200 && 400')
        
        
