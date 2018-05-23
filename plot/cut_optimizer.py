from efficiencies import Efficiencies
from styles import set_style

import copy
from ROOT import gPad

class CutOptimizer(object):
    
    def __init__(self, components, basecut, cuts):
        self.components = dict( (comp.name, comp) for comp in components)
        for comp in components:
            set_style(comp)
        self.basecut = basecut
        self.cuts = cuts
        
    def efficiencies(self, compname):
        comp = self.components[compname]
        eff = Efficiencies(comp.tree, self.cuts)
        eff.fill_cut_flow()
        print eff.str_cut_flow()
        
    def marginal(self, compname):
        comp = self.components[compname]
        eff = Efficiencies(comp.tree, self.cuts)
        eff.marginal()
        
    def draw_marginal(self, var, cutname):
        marg_cut = self.cuts.marginal(cutname).__str__()
        print marg_cut
        opt = 'norm'
        first = True
        maximum = 0
        hists = []
        for comp in self.components.values():
            print comp.name, '...'
            comp.tree.Draw(var, marg_cut, opt)
            hist = comp.tree.GetHistogram()
            hists.append(hist)
            comp.style.formatHisto(hist)
            if hist.GetMaximum() > maximum:
                maximum = hist.GetMaximum()
            if first:
                opt += 'same'
        hists[0].GetYaxis().SetRangeUser(0, maximum*1.2)
        gPad.Update()
