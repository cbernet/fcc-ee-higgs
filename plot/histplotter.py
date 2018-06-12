from itertools import count
import fnmatch

from ROOT import TPaveText, TH1

# from cpyroot import *
# from cpyroot.tools.style import *
from cpyroot.tools.DataMC.DataMCPlot import DataMCPlot
from fcc_ee_higgs.plot.plotter import histPref

##sZZ = Style(lineColor=4, fillColor=kBlue-9, fillStyle=3344)
##sZH= Style(lineColor=2, fillColor=5, fillStyle=0)
##sWW= Style(lineColor=6, fillStyle=3003)
##sffbar = Style(lineColor=1, fillStyle=3003)
##
##histPref = {
##    'ZZ*': {'style':sZZ, 'layer':10, 'legend':'ZZ'},
##    'WW*': {'style':sWW, 'layer':5, 'legend':'WW'},
##    'ZH*': {'style':sZH, 'layer':11, 'legend':'ZH'},
##    'ffbar': {'style':sffbar, 'layer':4, 'legend':'ffbar'},
##    'll': {'style':sffbar, 'layer':4, 'legend':'ll'},
##}

class HistPlotter(object):

    _ihist = count(0)
    
    def __init__(self, hists, lumi):
        self.hists = hists
        self.lumi = lumi
        self.styles = dict()
        self._set_styles()

    def _set_styles(self):
        for hist in self.hists:
            lsize = 0.05
            tsize = 0.06
            hist.GetXaxis().SetLabelSize(lsize)
            hist.GetXaxis().SetTitleSize(tsize)
            hist.GetYaxis().SetLabelSize(lsize)
            hist.GetYaxis().SetTitleSize(tsize)            
            hist.GetYaxis().SetTitleOffset(1.4)            
            found = False
            style = None
            for key, pref in histPref.iteritems():
                if fnmatch.fnmatch(hist.GetName(), key):
                    style = pref['style']
                    found = True
            if not found:
                style = sData
            self.styles[hist.GetName()] = style

    def _prepare_plot(self):
        plot = DataMCPlot('var', histPref)
        for hist in self.hists:
            name = hist.GetName()
            plot.AddHistogram(name, hist)
            plot.histosDict[name].SetWeight(1)
        plot.legendBorders = (0.22, 0.65, 0.44, 0.92)
        return plot
    
    def draw(self, xtitle='', ytitle=''):
        self.plot = self._prepare_plot()
        self.plot.DrawStack()
        self.plot.supportHist.GetXaxis().SetTitle(xtitle)
        self.plot.supportHist.GetYaxis().SetTitle(ytitle)
        
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
        
