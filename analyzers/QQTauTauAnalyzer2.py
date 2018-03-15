from heppy.framework.analyzer import Analyzer

import sys
import itertools
import pprint
import copy

from fcc_ee_higgs.analyzers.beta4 import beta4
from heppy.particles.tlv.resonance import Resonance2, Resonance
from heppy.particles.tlv.jet import Jet
from heppy.particles.jet import JetConstituents
from heppy.configuration import Collider

from ROOT import JetClusterizer 

class EventHypothesis(object):

    clusterizer = JetClusterizer(1)
    
    def __init__(self, taus, jets):
        qqjetsp = [jet for jet in jets if jet not in taus]
        # assert(len(qqjetsp) == 2)
        self.zed = Resonance(qqjetsp, 23, 1)  
        self.higgs = Resonance2(taus[0], taus[1], 25, 1)
        self.taus = taus
        
    def force_2_jets(self, particles):
        self.__class__.clusterizer.clear()
        other_particles = []
        for ptc in particles:
            keep = True
            for tau in self.taus:
                if ptc in tau.constituents.particles:
                    keep = False
            if keep:
                self.__class__.clusterizer.add_p4(ptc.p4())
                other_particles.append(ptc)
        assert(len(other_particles)
               + len(self.taus[0].constituents.particles)
               + len(self.taus[1].constituents.particles) == len(particles))
        njets = 2
        if len(other_particles) < njets:
            return False
        self.__class__.clusterizer.make_exclusive_jets(njets) 
        assert(self.__class__.clusterizer.n_jets() == njets)
        jets = []
        for jeti in range(self.__class__.clusterizer.n_jets()):
            jet = Jet( self.__class__.clusterizer.jet(jeti) )
            jet.constituents = JetConstituents()
            for consti in range(self.__class__.clusterizer.n_constituents(jeti)):
                constituent_index = self.__class__.clusterizer.constituent_index(jeti, consti)
                constituent = particles[constituent_index]
                jet.constituents.append(constituent)
            jet.constituents.sort()            
            jets.append( jet )
        self.jets2 = jets
        self.zed2 = Resonance2(jets[0], jets[1], 23, 1)
        return True
    
    def beta4_rescale(self):
        all_jets = list(self.jets2)
        all_jets.extend(self.taus)
        jets_rescaled = copy.deepcopy(all_jets)
        beta4(jets_rescaled, Collider.SQRTS)
        self.jets2_r = jets_rescaled[:2]
        self.taus_r = jets_rescaled[2:]
        self.zed2_r = Resonance2(self.jets2_r[0], self.jets2_r[1], 23, 1)
        self.higgs_r = Resonance2(self.taus_r[0], self.taus_r[1], 25, 1)      
            
class QQTauTauAnalyzer2(Analyzer):

    def beginLoop(self, setup):
        super(QQTauTauAnalyzer2, self).beginLoop(setup)
        self.counters.addCounter('cutflow')
        self.counters['cutflow'].register('All events')
        self.counters['cutflow'].register('2 taus')
        self.counters['cutflow'].register('3 taus')
        self.counters['cutflow'].register('4 taus')
        
    def process(self, event):
        jets = getattr(event, self.cfg_ana.jets)
        taus = getattr(event, self.cfg_ana.taus)
        particles = getattr(event, self.cfg_ana.particles)
        self.counters['cutflow'].inc('All events')
        if len(taus) < 2:
            return False
        self.counters['cutflow'].inc('2 taus')
        if len(taus) == 3:
            self.counters['cutflow'].inc('3 taus')
        elif len(taus) == 4:
            self.counters['cutflow'].inc('4 taus')
        dmz = sys.float_info.max
        event_hypos = []
        for taus in itertools.combinations(taus, 2):
            hypo = EventHypothesis(taus, jets)
            forced = hypo.force_2_jets(particles)
            if not forced:
                continue
            hypo.beta4_rescale()
            event_hypos.append(hypo)
        if len(event_hypos) == 0:
            return False
        event_hypos.sort(key=lambda hyp: abs(hyp.zed2_r.m() - 91))
        best_hyp = event_hypos[0]
        setattr(event, 'bestjets', [best_hyp.zed2_r.leg1(),
                                    best_hyp.zed2_r.leg2()])
        setattr(event, 'besttaus', [best_hyp.higgs_r.leg1(),
                                    best_hyp.higgs_r.leg2()])
        setattr(event, 'zedqq', [best_hyp.zed])
        setattr(event, 'zedqq2', [best_hyp.zed2])
        setattr(event, 'zedqq2_r', [best_hyp.zed2_r])
        setattr(event, 'higgs', [best_hyp.higgs])        
        setattr(event, 'higgs_r', [best_hyp.higgs_r])        

