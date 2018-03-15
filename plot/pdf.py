from ROOT import gPad

class PDF(object):
    
    def __init__(self, comps):
        self.comps = dict((comp.name, comp) for comp in comps)
        
    def draw(self, var, cut):
        same = ''
        hists = []
        for comp in self.comps.values():
            comp.tree.Draw(var, cut, 'histnorm'+same)
            hist = comp.tree.GetHistogram()
            hists.append(hist)
            if hasattr(comp, 'style'):
                comp.style.formatHisto(hist)
            if same == '':
                var = var.split('>>')[0]
                same = 'same'
        maxy = max(h.GetMaximum() for h in hists)
        hists[0].GetYaxis().SetRangeUser(0, maxy*1.1)
        gPad.Modified()
        gPad.Update()
