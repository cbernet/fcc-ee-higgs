import unittest

from fcc_ee_higgs.plot.efficiencies import Efficiencies

# getting a test tree
import os
from ROOT import TFile
test_fname = os.path.dirname(__file__) + '/test_data/tree_genf_e0.root'
test_file = TFile(test_fname)
tree = test_file.Get('events')

# getting cuts
from fcc_ee_higgs.plot.plotconfig_ZH_lltautau import cut_lepiso, cut_z_mass, cut_z_kine
cuts = dict(
    cut_lepiso=cut_lepiso,
    cut_z_mass=cut_z_mass, 
    cut_z_kine=cut_z_kine
)

class TestEfficiencies(unittest.TestCase):
        
    def test_1(self):
        eff = Efficiencies(tree, cuts)
        eff.marginal()

if __name__ == '__main__':
    unittest.main()
