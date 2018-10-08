from heppy.framework.analyzer import Analyzer

import pprint
from ROOT import TLorentzVector

class FSRRecovery(Analyzer):
    
    def process(self, event):
        leptons = getattr(event, self.cfg_ana.leptons)
        photons = getattr(event, self.cfg_ana.photons)
        area = self.cfg_ana.area
        for lepton in leptons:
            for photon in photons:
                pass
