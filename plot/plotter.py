from itertools import count
import fnmatch

from ROOT import TPaveText, TH1

from cpyroot import *
from cpyroot.tools.style import *
from cpyroot.tools.DataMC.DataMCPlot import DataMCPlot

sZZ = Style(lineColor=4, fillColor=kBlue-9, fillStyle=3344)
sZH= Style(lineColor=2, fillColor=10, fillStyle=0)
sWW= Style(lineColor=6, fillStyle=3003)
sffbar = Style(lineColor=1, fillStyle=3003)

histPref = {
    'ZZ*': {'style':sZZ, 'layer':10, 'legend':'ZZ'},
    'WW*': {'style':sWW, 'layer':5, 'legend':'WW'},
    'ZH*': {'style':sZH, 'layer':11, 'legend':'ZH'},
    'ffbar': {'style':sffbar, 'layer':4, 'legend':'ffbar'},
    'll': {'style':sffbar, 'layer':4, 'legend':'ll'},
}

class Plotter(object):

    _ihist = count(0)
    
    def __init__(self, comps, lumi):
        self.comps = comps
        self.lumi = lumi
        self._set_styles()

    def _set_styles(self):
        for comp in self.comps:
            found = False
            for key, pref in histPref.iteritems():
                if fnmatch.fnmatch(comp.name, key):
                    comp.style = pref['style']
                    found = True
            if not found:
                comp.style = sData
                
    def _project(self, comp, var, cut, *bins):
        # hist_name = '{}_{}'.format(comp.name, self._ihist.next())
        hist_name = comp.name
        hist = TH1F(hist_name, '', *bins)
        if comp.tree != None:
            comp.tree.Project(hist.GetName(), var, cut)
        print hist_name
        return hist

    def _prepare_plot(self, var, cut, bins):
        plot = DataMCPlot('recoil', histPref)
        for comp in self.comps:
            hist = self._project(comp, var, cut, *bins)    
            plot.AddHistogram(comp.name, hist)
            plot.histosDict[comp.name].SetWeight(comp.getWeight(self.lumi).GetWeight())
            plot.histosDict[comp.name].uncertainty = comp.uncertainty
        plot.legendBorders = (0.22, 0.65, 0.44, 0.92)
        return plot
    
    def draw(self, var, cut, bins, xtitle='', ytitle=''):
        self.plot = self._prepare_plot(var, cut, bins)
        self.plot.DrawStack()
        # self.plot.supportHist.GetYaxis().SetTitleOffset(1.35)
        # self.plot.supportHist.GetYaxis().SetNdivisions(5)
        # self.plot.supportHist.GetXaxis().SetNdivisions(5)
        self.plot.supportHist.GetXaxis().SetTitle(xtitle)
        self.plot.supportHist.GetYaxis().SetTitle(ytitle)
        print 'variable:'
        print var
        print 'cut:'
        print cut
        
        
    def print_info(self, detector, xmin=None, ymin=None):
        lumitext = ''
        lumi = self.lumi
        if lumi > 1e15:
            lumi = int(self.lumi / 1e15)
            lumitext = '{lumi} ab^{{-1}}'.format(lumi=lumi)
        elif lumi > 1e12:
            lumi = int(self.lumi / 1e12)
            lumitext = '{lumi} fb^{{-1}}'.format(lumi=lumi)            
        if not xmin:
            xmin = 0.62
        if not ymin:
            ymin = 0.8
        xmax, ymax = xmin + 0.288, ymin + 0.12
        self.pave = TPaveText(xmin, ymin, xmax, ymax, 'ndc')
        self.pave.AddText(detector)
        self.pave.AddText(lumitext)
        self.pave.SetTextSizePixels(28)
        self.pave.SetTextAlign(11)
        self.pave.SetBorderSize(0)
        self.pave.SetFillColor(0)
        self.pave.SetFillStyle(0)
        self.pave.Draw()
        
