from itertools import count
import fnmatch

from ROOT import TPaveText, TH1

from cpyroot import *
from cpyroot.tools.DataMC.DataMCPlot import DataMCPlot

from styles import set_style, histPref

class Plotter(object):

    _ihist = count(0)
    
    def __init__(self, comps, lumi):
        self.comps = comps
        for comp in self.comps:
            set_style(comp)
        self.lumi = lumi
                
    def _project(self, comp, var, cut, *bins):
        # hist_name = '{}_{}'.format(comp.name, self._ihist.next())
        hist_name = comp.name
        hist = TH1F(hist_name, '', *bins)
        if comp.tree != None:
            comp.tree.Project(hist.GetName(), var, cut)
        print hist_name, comp.rootfile
        return hist

    def _prepare_plot(self, var, cut, bins):
        plot = DataMCPlot('var', histPref)
        for comp in self.comps:
            hist = self._project(comp, var, cut, *bins)
            if hasattr(comp, 'smooth') and comp.smooth:    
                hist.Smooth(comp.smooth)
            if hasattr(comp, 'preprocess'):
                hist = comp.preprocess(hist)
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
        
    def write(self, fname):
        the_file = open(fname, 'w')
        the_file.write(str(self.plot))
        the_file.close()
       
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
        
