
from heppy.framework.analyzer import Analyzer
from heppy.configuration import Collider

import copy
import math

from fcc_ee_higgs.analyzers.beta4 import beta4

class Beta4Rescaler(Analyzer):

    def process(self, event):
        jets = getattr(event, self.cfg_ana.jets)
        if not len(jets) == 4:
            return False
        chi2 = -1
        sqrts = Collider.SQRTS
        jets_rescaled = copy.deepcopy(jets)
        for jr, j in zip(jets_rescaled, jets):
            jr.raw = j
        chi2 = beta4(jets_rescaled, sqrts)
        for jet in jets_rescaled:
            if jet.e() < 0:
                return False
        setattr(event, self.cfg_ana.output, jets_rescaled)
        setattr(event, 'beta4_chi2', chi2)
 
        
