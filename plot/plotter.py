from cpyroot import *

from cpyroot.tools.style import *
from cpyroot.tools.DataMC.DataMCPlot import DataMCPlot

sZZ = Style(lineColor=4, fillColor=kBlue-9, fillStyle=3344)
sZH= Style(lineColor=2, fillColor=10, fillStyle=1001)
sWW= Style(lineColor=6, fillStyle=3003)
sffbar = Style(lineColor=6, fillStyle=3003)

histPref = {
    'ZZ*': {'style':sZZ, 'layer':10, 'legend':'ZZ'},
    'WW*': {'style':sWW, 'layer':5, 'legend':'WW'},
    'ZH*': {'style':sZH, 'layer':11, 'legend':'ZH'},
    'ffbar': {'style':sffbar, 'layer':4, 'legend':'ffbar'},
}

class Plotter(object):
    
    def __init__(self, comps, lumi):
        self.comps = comps
        self.lumi = lumi
        self.papaslabel = TLatex()

    def _project(self, comp, var, cut, *bins):
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
        plot.legendBorders = (0.22, 0.65, 0.44, 0.92)
        return plot
    
    def draw(self, var, cut, bins, title='', label=''):
        self.plot = self._prepare_plot(var, cut, bins)
        self.plot.DrawStack()
        # self.plot.supportHist.GetYaxis().SetTitleOffset(1.35)
        # self.plot.supportHist.GetYaxis().SetNdivisions(5)
        # self.plot.supportHist.GetXaxis().SetNdivisions(5)
        self.plot.supportHist.GetXaxis().SetTitle(title)
        self.papaslabel.DrawLatexNDC(0.60, 0.88, label)
        print var, cut 
        
