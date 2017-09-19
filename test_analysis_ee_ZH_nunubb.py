import unittest
import tempfile
import copy
import os
import shutil

import heppy.framework.context as context

if context.name == 'fcc':

    from analysis_ee_ZH_nunubb_cfg import config, test_filename
    from heppy.framework.looper import Looper
    from ROOT import TFile

    import logging
    logging.getLogger().setLevel(logging.ERROR)

    import heppy.statistics.rrandom as random

    class TestAnalysis_ee_ZH_nunubb(unittest.TestCase):

        def setUp(self):
            random.seed(0xdeadbeef)
            self.outdir = tempfile.mkdtemp()
            import logging
            logging.disable(logging.CRITICAL)

        def tearDown(self):
            shutil.rmtree(self.outdir)
            logging.disable(logging.NOTSET)

        def test_1(self):
            '''Check that the ZH->nunubb analysis runs
            '''
            from heppy.papas.detectors.CMS import cms
            config.components[0].files = [test_filename]
            for s in config.sequence:
                if hasattr( s,'detector'):
                    s.detector = cms
            self.looper = Looper( self.outdir, config,
                                  nEvents=10,
                                  nPrint=0 )
            self.looper.loop()
            self.looper.write()

 

        

if __name__ == '__main__':

    unittest.main()
