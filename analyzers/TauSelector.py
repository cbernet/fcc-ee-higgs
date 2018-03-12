from heppy.framework.analyzer import Analyzer

import pprint

class TauSelector(Analyzer):
    
    def process(self, event):
        jets = getattr(event, self.cfg_ana.jets)
        taus = []
        ids = [211, 11, 13]  # e and mu treated as taus
        for jet in jets:
            csts = jet.constituents
            ncharged = sum(csts[the_id].num() for the_id in ids)
            if self.cfg_ana.verbose:
                print csts
            if ncharged == 1 or ncharged == 3:
                taus.append(jet)
                if self.cfg_ana.verbose:
                    print '... is tau'
            elif self.cfg_ana.verbose:
                print '... is not tau'
        setattr(event, self.cfg_ana.output, taus)
