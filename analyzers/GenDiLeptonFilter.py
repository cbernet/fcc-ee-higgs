from heppy.framework.analyzer import Analyzer

class GenDiLeptonFilter(Analyzer):
    
    def process(self, event):
        '''Select events with at least 2 electrons 
        or at least two muons 
        '''
        eles = getattr(event, self.cfg_ana.eles)
        mus = getattr(event, self.cfg_ana.mus)
        return len(eles) >= 2 or len(mus) >= 2
        
