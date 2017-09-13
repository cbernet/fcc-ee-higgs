import unittest
import tempfile
import copy
import os
import shutil

import heppy.framework.context as context

if context.name == 'fcc':

    from analysis_ee_Z_cfg import config
    from heppy.test.plot_ee_Z import plot_ee_mass
    from heppy.framework.looper import Looper
    from ROOT import TFile

    import logging
    logging.getLogger().setLevel(logging.ERROR)

    import heppy.statistics.rrandom as random

    class TestAnalysis_ee_Z(unittest.TestCase):

        def setUp(self):
            random.seed(0xdeadbeef)
            self.outdir = tempfile.mkdtemp()
            import logging
            logging.disable(logging.CRITICAL)

        def tearDown(self):
            shutil.rmtree(self.outdir)
            logging.disable(logging.NOTSET)

        def test_z_1_cms(self):
            '''Check Z mass in ee->Z->ddbar (CMS).
            Will fail if physics algorithms are modified,
            so should probably be removed from test suite,
            or better: be made optional. 
            '''
            from heppy.papas.detectors.CMS import cms
            fname = 'ee_ffbar.root'
            config.components[0].files = [fname]
            for s in config.sequence:
                if hasattr( s,'detector'):
                    s.detector = cms
            self.looper = Looper( self.outdir, config,
                                  nEvents=100,
                                  nPrint=0 )
            self.looper.loop()
            self.looper.write()
            rootfile = '/'.join([self.outdir,
                                'heppy.analyzers.GlobalEventTreeProducer.GlobalEventTreeProducer_1/tree.root'])
            mean, sigma = plot_ee_mass(rootfile)
            self.assertAlmostEqual(mean, 94.7, 1)
            self.assertAlmostEqual(sigma, 15.1, 1)

 

        

if __name__ == '__main__':

    unittest.main()
