import unittest
import tempfile
import copy
import os
import shutil

import heppy.framework.context as context

if context.name == 'fcc':

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
            import logging
            logging.disable(logging.CRITICAL)

        def tearDown(self):
            shutil.rmtree(self.outdir)
            logging.disable(logging.NOTSET)

        def test_ZH_mumubb(self):
            '''Check that the ZH mumubb analysis runs
            '''
            from analysis_ee_ZH_cfg import config
            fname = '/Users/cbernet/Code/FCC/fcc_ee_higgs/samples/pythia/ZH/ee_ZH_Zmumu_1.root'
            config.components[0].files = [fname]
            looper = Looper( self.outdir, config,
                             nEvents=50,
                             nPrint=0,
                             timeReport=True)            
            looper.loop()
            looper.write()
            
        def test_ZH_nunubb(self):
            '''Check that the ZH nunubb analysis runs
            '''
            from analysis_ee_ZH_nunubb_cfg import config
            fname = 'samples/pythia/examples/ee_ZH_Znunu.root'
            config.components[0].files = [fname]
            looper = Looper( self.outdir, config,
                             nEvents=50,
                             nPrint=0,
                             timeReport=True)            
            looper.loop()
            looper.write()


if __name__ == '__main__':

    unittest.main()
