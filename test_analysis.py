import unittest
import tempfile
import copy
import os
import shutil

import heppy.framework.context as context

from analysis_test_beamsmearer import config
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
        config.components = config.components[:1]
        config.components[0].files = config.components[0].files[:1]
        self.looper = Looper( self.outdir,
                              config,
                              nEvents=10,
                              nPrint=3)
        self.looper.loop()
        self.looper.write()

 

        

if __name__ == '__main__':

    unittest.main()
