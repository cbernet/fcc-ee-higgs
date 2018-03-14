from heppy.framework.analyzer import Analyzer

import pprint

class TauSelector(Analyzer):
    
    def beginLoop(self, setup):
        super(TauSelector, self).beginLoop(setup)
        self.counters.addCounter('cutflow')
        self.counters['cutflow'].register('All events')
        self.counters['cutflow'].register('2 taus')
        self.counters['cutflow'].register('3 taus')
        self.counters['cutflow'].register('4 taus')
        
    def process(self, event):
        self.counters['cutflow'].inc('All events') 
        jets = getattr(event, self.cfg_ana.jets)
        taus = []
        ids = [211, 11, 13]  # e and mu treated as taus
        for jet in jets:
            csts = jet.constituents
            ncharged = sum(csts[the_id].num() for the_id in ids)
            if self.cfg_ana.verbose:
                print jet
                for ptc in csts.particles:
                    print '\t', ptc
                print csts
            if ncharged == 1 or ncharged == 3:
                taus.append(jet)
                if self.cfg_ana.verbose:
                    print '... is tau'
            elif self.cfg_ana.verbose:
                print '... is not tau'
        if self.cfg_ana.verbose:
            print 'n taus:', len(taus)
        if len(taus) == 2:
            self.counters['cutflow'].inc('2 taus')
        elif len(taus) == 3:
            self.counters['cutflow'].inc('3 taus')
        elif len(taus) == 4:
            self.counters['cutflow'].inc('4 taus')
            
        setattr(event, self.cfg_ana.output, taus)
