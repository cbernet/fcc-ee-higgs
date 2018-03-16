import unittest

from fcc_ee_higgs.plot.pdf import PDF
from cpyroot import sBlack, sBlue
import os
from ROOT import TFile

sBlack.fillStyle = 0
sBlue.fillStyle = 0

class Component(object):
    def __init__(self, name, fname):
        self.name = name 
        self.tfile = TFile(fname)
        self.tree = self.tfile.Get('events')
c1 = Component('zh', os.path.dirname(__file__) + '/test_data/zh_qqtautau.root')
c2 = Component('ww', os.path.dirname(__file__) + '/test_data/ww_qqtautau.root')
c1.style = sBlack
c2.style = sBlue

pdf = PDF([c1, c2])

class TestPDF(unittest.TestCase):
        
    def test_1(self):
        pdf.draw('higgs_m','higgs_m<200')
        

if __name__ == '__main__':
    unittest.main()
