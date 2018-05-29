from heppy.framework.analyzer import Analyzer
from heppy.statistics.counter import Counter

class FinalSelection(Analyzer):

    def beginLoop(self, setup):
        super(FinalSelection, self).beginLoop(setup)
        self.counters.addCounter('hyp_rec') 
        self.counters['hyp_rec'].register('All events')
        self.counters['hyp_rec'].register('Successful rescaling')
        self.counters['hyp_rec'].register('not ZZ or WW')
        self.counters['hyp_rec'].register('mH jet>100')
        self.counters['hyp_rec'].register('80<mZ jet<110')  
        self.counters['hyp_rec'].register('higgs made')
    
    def process(self, event):
        self.counters['hyp_rec'].inc('All events')
        jets = event.hjets
        if event.chi2 < 0:
            return True
        self.counters['hyp_rec'].inc('Successful rescaling')

        if event.deltaWW <= 10 or event.deltaZZ <= 10:
            return True
        self.counters['hyp_rec'].inc('not ZZ or WW')

        recos = 0
        for jet in jets:
            if jet.tags['b'] and jet.tags['higgsmaker']:
                recos += 1
        if recos != 2: return True
        if not(event.mHJet > 100):
            return True
        self.counters['hyp_rec'].inc('mH jet>100')
        if not(event.mZedJet > 80 and event.mZedJet < 110): return True
        self.counters['hyp_rec'].inc('80<mZ jet<110')
        
        if event.higgsmass<=0: return True
        self.counters['hyp_rec'].inc('higgs made')
