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
        output = []
        for b in bosons:
            assert(len(b.daughters) == 2)
            if hasattr(self.cfg_ana, 'decay_pdgids') and \
               not ( abs(b.daughters[0].pdgid()) in self.cfg_ana.decay_pdgids and \
                     abs(b.daughters[1].pdgid()) in self.cfg_ana.decay_pdgids ):
                continue
            resonance = Resonance2(b.daughters[0],
                                   b.daughters[1],
                                   b.pdgid(), b.status())
            output.append(resonance)
        output.sort(key=lambda x: x.pdgid())
        output_name = 'genbosons'
        if hasattr(self.cfg_ana, 'output'):
            output_name = self.cfg_ana.output
        setattr(event, output_name, output)
        if self.verbose:
            print self
            if not len(output):
                print 'no boson found'
            else:
                for gb in output:
                    print gb
                    pprint.pprint(gb.legs)
            print
            
            
