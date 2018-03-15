from heppy.framework.analyzer import Analyzer
from heppy.particles.tlv.resonance import Resonance2
from heppy.particles.genbrowser import GenBrowser

import pprint

class GenResonanceAnalyzer(Analyzer):

    def process(self, event):
        bosons = [ptc for ptc in event.gen_particles
                  if abs(ptc.pdgid()) in self.cfg_ana.pdgids
                  and ptc.status() in self.cfg_ana.statuses]
        if not hasattr(event, 'genbrowser'):
            event.genbrowser = GenBrowser(event.gen_particles,
                                          event.gen_vertices)
        event.gen_bosons = []
        for b in bosons:
            assert(len(b.daughters) == 2)
            if hasattr(self.cfg_ana, 'decay_pdgids') and \
               not ( abs(b.daughters[0].pdgid()) in self.cfg_ana.decay_pdgids and \
                     abs(b.daughters[1].pdgid()) in self.cfg_ana.decay_pdgids ):
                continue
            resonance = Resonance2(b.daughters[0], b.daughters[1],
                                   b.pdgid(), b.status())
            event.gen_bosons.append(resonance)
        event.gen_bosons.sort(key=lambda x: x.pdgid())
        if self.verbose:
            print self
            if not len(event.gen_bosons):
                print 'no boson found'
            else:
                for gb in event.gen_bosons:
                    print gb
                    pprint.pprint(gb.legs)
            print
            
            
