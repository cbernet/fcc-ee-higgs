from heppy.framework.analyzer import Analyzer

import sys
import itertools
import pprint
import copy

from heppy.particles.tlv.resonance import Resonance2, Resonance
from heppy.analyzers.ResonanceBuilder import mass

class EventHypothesis(object):
    
    def __init__(self, hid, w_jets, wstar_jets):
        self.hid = hid
        self.w_jets = w_jets
        self.wstar_jets = wstar_jets
        self.w = Resonance2(self.w_jets[0], self.w_jets[1], 24)
        self.wstar = Resonance2(self.wstar_jets[0], self.wstar_jets[1], 24)

class NuNuWWAnalyzer(Analyzer):

    def process(self, event):
        jets = getattr(event, self.cfg_ana.jets)
        hypos = []
        for hid, w_jets in enumerate(itertools.combinations(jets, 2)):
            wstar_jets = [jet for jet in jets if jet not in w_jets]
            hypo = EventHypothesis(hid, w_jets, wstar_jets)
            hypos.append(hypo)
        best_hypo = min(hypos, key=lambda x: abs(x.w.m() - mass[24]))
        setattr(event, 'w', best_hypo.w)
        setattr(event, 'wstar', best_hypo.wstar)
        
