from heppy.framework.analyzer import Analyzer

import sys
import itertools
import pprint
import copy

from fcc_ee_higgs.analyzers.beta4 import beta4
from heppy.configuration import Collider
from heppy.particles.tlv.resonance import Resonance2

class LLTauTauAnalyzer(Analyzer):
    
    def process(self, event):
        zeds = getattr(event, self.cfg_ana.zeds)
        higgses = getattr(event, self.cfg_ana.higgses)
        zed = zeds[0]
        higgs = higgses[0]
        all_objects = list(zed.legs)
        all_objects.extend(higgs.legs)
        all_objects_rescaled = copy.deepcopy(all_objects)
        beta4(all_objects_rescaled, Collider.SQRTS)
        zed_legs_r = all_objects_rescaled[:2]
        higgs_legs_r = all_objects_rescaled[2:]
        zed_r = Resonance2(zed_legs_r[0], zed_legs_r[1], 23, 1)
        higgs_r = Resonance2(higgs_legs_r[0], higgs_legs_r[1], 25, 1)      
        setattr(event, self.cfg_ana.zeds+'_r', [zed_r])
        setattr(event, self.cfg_ana.higgses+'_r', [higgs_r])
        
