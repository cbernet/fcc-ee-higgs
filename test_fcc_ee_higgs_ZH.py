import unittest
import tempfile
import copy
import os
import shutil

import heppy.framework.context as context

if context.name == 'fcc':

    from analysis_ee_ZH_cfg import config
    from heppy.test.plot_ee_ZH import plot
    from heppy.framework.looper import Looper
    from ROOT import TFile

    import logging
    logging.getLogger().setLevel(logging.ERROR)

    import heppy.statistics.rrandom as random

    def test_sorted(ptcs):
        from heppy.configuration import Collider
        keyname = 'pt'
        if Collider.BEAMS == 'ee':
            keyname = 'e'
        pt_or_e = getattr(ptcs[0].__class__, keyname)
        values = [pt_or_e(ptc) for ptc in ptcs]
        return values == sorted(values, reverse=True)


    class Test_fcc_ee_higgs_ZH(unittest.TestCase):

        def setUp(self):
            random.seed(0xdeadbeef)
            self.outdir = tempfile.mkdtemp()
            fname = 'ee_ZH_Z_Hbb.root'
            # fname = '/Users/cbernet/Code/FCC/fcc_ee_higgs/samples/pythia/ZZ/ee_ZZ_3.root'
            config.components[0].files = [fname]
            self.looper = Looper( self.outdir, config,
                                  nEvents=50,
                                  nPrint=0,
                                  timeReport=True)
            import logging
            logging.disable(logging.CRITICAL)

        def tearDown(self):
            shutil.rmtree(self.outdir)
            logging.disable(logging.NOTSET)

        def test_analysis(self):
            '''Check for an almost perfect match with reference.
            Will fail if physics algorithms are modified,
            so should probably be removed from test suite,
            or better: be made optional. 
            '''        
            self.looper.loop()
            self.looper.write()
            


if __name__ == '__main__':

    unittest.main()
