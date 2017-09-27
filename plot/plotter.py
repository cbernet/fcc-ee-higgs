from cpyroot import *

from cpyroot.tools.style import *
from cpyroot.tools.DataMC.DataMCPlot import DataMCPlot

histPref = {
    'ZZ*': {'style':sBlue, 'layer':10, 'legend':'ZZ'},
    'WW*': {'style':sRed, 'layer':5, 'legend':'WW'},
    'ZH*': {'style':sGreen, 'layer':11, 'legend':'ZH'},
    'ffbar': {'style':sRed, 'layer':4, 'legend':'ffbar'},
}

class Plotter(object):
    
    def __init__(self, comps, lumi):
        self.comps = comps
        self.lumi = lumi
##        for comp in self.comps:
##            self._load(comp)
           
##    def _load(self, comp, basedir):
##        comp.directory = '/'.join([basedir, comp.name])
##        print comp.directory
##        comp.rootfile = TFile('{}/{}'.format(
##            comp.directory,
##            'heppy.analyzers.examples.zh.ZHTreeProducer.ZHTreeProducer_1/tree.root'
##        ))
##        comp.tree = comp.rootfile.Get('events')
##        print comp
##        print '-'
    
##    def _load(self, comp):
##        print 'warning convert to Chain!'
##        comp.rootfile = TFile(comp.files[0])
##        comp.tree = comp.rootfile.Get('events')
##        print comp
##        print '-'


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
    
    def draw(self, var, cut, bins, title=''):
        self.plot = self._prepare_plot(var, cut, bins)
        self.plot.DrawStack()
        self.plot.supportHist.GetYaxis().SetTitleOffset(1.35)
        self.plot.supportHist.GetYaxis().SetNdivisions(5)
        self.plot.supportHist.GetXaxis().SetNdivisions(5)
        self.plot.supportHist.GetXaxis().SetTitle(title)
        print var, cut 
        
