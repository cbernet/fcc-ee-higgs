
from heppy.framework.analyzer import Analyzer
from heppy.configuration import Collider
from ROOT import TLorentzVector

import copy
import math

from fcc_ee_higgs.analyzers.beta4 import beta4

class Beta4Rescaler(Analyzer):

    def process(self, event):
        jets = getattr(event, self.cfg_ana.jets)
        chi2 = -1
        if len(jets) == 4:
            sqrts = Collider.SQRTS
            jets_rescaled = copy.deepcopy(jets)
            chi2 = beta4(jets_rescaled, sqrts)
        else:
            jets_rescaled = jets
        setattr(event, self.cfg_ana.output, jets_rescaled)
        setattr(event, 'beta4_chi2', chi2)
 
        
