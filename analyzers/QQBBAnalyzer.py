from heppy.framework.analyzer import Analyzer

import sys
import itertools
import pprint
import copy

from heppy.particles.tlv.resonance import Resonance2, Resonance

class EventHypothesis(object):
    
    def __init__(self, hid, higgs_jets, zed_jets):
        self.hid = hid
        self.higgs_jets = higgs_jets
        self.zed_jets = zed_jets
        if self.higgs_jets[0].tags['bfrac'] > 0.05 and \
           self.higgs_jets[1].tags['bfrac'] > 0.05:
            self.is_true = True
        else:
            self.is_true = False
        self.higgs = Resonance2(self.higgs_jets[0], self.higgs_jets[1], 25)
        self.zed = Resonance2(self.zed_jets[0], self.zed_jets[1], 23)

class QQBBAnalyzer(Analyzer):

    def process(self, event):
        jets = getattr(event, self.cfg_ana.jets)
        hypos = []
        for hid, higgs_jets in enumerate(itertools.combinations(jets, 2)):
            zed_jets = [jet for jet in jets if jet not in higgs_jets]
            hypo = EventHypothesis(hid, higgs_jets, zed_jets)
            hypos.append(hypo)
        true_hypos = [hypo for hypo in hypos if hypo.is_true is True]
        print 'number of true hypotheses', len(true_hypos)
        if len(true_hypos) == 0:
            print 'No true hypo'
            return False
        elif len(true_hypos) > 1:
            print 'More than 1 true hypo'
            return False
        setattr(event, 'hypotheses', hypos)
        
