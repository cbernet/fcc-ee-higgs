import unittest
import tempfile
import copy
import os
import shutil

import heppy.framework.context as context

from analysis_ee_ZH_qqbb import config, test_filename
from heppy.framework.looper import Looper
from ROOT import TFile

# no_printout = False

import logging
logging.getLogger().setLevel(logging.INFO)

import heppy.statistics.rrandom as random

class TestAnalysis(unittest.TestCase):

    def setUp(self):
        random.seed(0xdeadbeef)
        self.outdir = tempfile.mkdtemp()
        # logging.disable(logging.CRITICAL)

    def tearDown(self):
        shutil.rmtree(self.outdir)
        # logging.disable(logging.NOTSET)

    def test_1(self):
        '''Check that the ZH->nunubb analysis runs
        '''
##        # from heppy.papas.detectors.CMS import cms
##        # config.components[0].files = [test_filename]
##        for s in config.sequence:
##            if hasattr( s,'detector'):
##                s.detector = cms
        self.looper = Looper( self.outdir,
                              config,
                              nEvents=10,
                              nPrint=10 )
        self.looper.loop()
        self.looper.write()

 

        

if __name__ == '__main__':

    unittest.main()
