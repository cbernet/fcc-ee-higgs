from heppy.framework.analyzer import Analyzer

class GenDiLeptonFilter(Analyzer):
    
    def process(self, event):
        '''Select events with at least 2 electrons 
        or at least two muons 
        '''
        same_flavour  = True
        if hasattr(self.cfg_ana, 'same_flavour '):
            same_flavour  = self.cfg_ana.same_flavour 
        eles = getattr(event, self.cfg_ana.eles)
        mus = getattr(event, self.cfg_ana.mus)
        result = None
        if same_flavour :
            result = len(eles) >= 2 or len(mus) >= 2
        else:
            result = len(eles) + len(mus) >= 2
