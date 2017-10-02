from heppy.framework.analyzer import Analyzer
from heppy.particles.tlv.resonance import Resonance2
from heppy.particles.genbrowser import GenBrowser

class GenResonanceAnalyzer(Analyzer):

    def process(self, event):
        bosons = [ptc for ptc in event.gen_particles
                  if ptc.pdgid() in self.cfg_ana.pdgids
                  and ptc.status() in self.cfg_ana.statuses]
        if not hasattr(event, 'genbrowser'):
            event.genbrowser = GenBrowser(event.gen_particles,
                                          event.gen_vertices)
        event.gen_bosons = []
        for b in bosons:
            assert(len(b.daughters) == 2)
            resonance = Resonance2(b.daughters[0], b.daughters[1],
                                   b.pdgid(), b.status())
            event.gen_bosons.append(resonance)
            
