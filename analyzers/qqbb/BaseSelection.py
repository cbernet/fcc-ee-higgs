from heppy.framework.analyzer import Analyzer
from heppy.statistics.counter import Counter

class BaseSelection(Analyzer):

    def beginLoop(self, setup):
        super(BaseSelection, self).beginLoop(setup)
        self.counters.addCounter('base_sel') 
        self.counters['base_sel'].register('All events')
        self.counters['base_sel'].register('no lepton')
        self.counters['base_sel'].register('4 jets')
        self.counters['base_sel'].register('jet ID')
        self.counters['base_sel'].register('2 b jets')
        self.counters['base_sel'].register('mvis > 180')
    
    def process(self, event):
        self.counters['base_sel'].inc('All events')
        if len(event.sel_iso_leptons) > 2:
            return True # could return False to stop processing
        else:
            self.counters['base_sel'].inc('no lepton')
        
        if len(event.jets_inclusive) >= 4:
            self.counters['base_sel'].inc('4 jets')
        else:
            return True
        
        jetid = True
        for jet in event.jets:
            if not (jet.tags['n_constituents'] >= 5 and \
                    jet.tags['n_charged_hadrons'] > 0):
                jetid = False
        if jetid:
            self.counters['base_sel'].inc('jet ID')
        else:
            return True
        
        if len(event.bjets) >= 2:
            self.counters['base_sel'].inc('2 b jets')
        else:
            return True

        if event.sum_vis.m() >= 180:
            self.counters['base_sel'].inc('mvis > 180')
        else:
            return True 
        
