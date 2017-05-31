from cpyroot.tools.DataMC import DataMCPlot, Histogram
from ROOT import RooRealVar, RooDataSet, RooDataHist, RooHistPdf, RooGaussian, RooArgSet, RooAddPdf, RooArgList, RooFit

class Fitter(object):

    def __init__(self, plot):
        assert(isinstance(plot, DataMCPlot))
        self.plot = plot
        self._make_model()
        self._make_dataset()
        self._fit()

    def _make_model(self):
        self.pdfs = {}
        self.yields = {}
        nbins, xmin, xmax = self.plot.histos[0].GetBinning()
        self.xvar = RooRealVar("x", "x", xmin, xmax)
        self.xvar.setBins(nbins)
        self.pdfs = {}        
        for compname, comp in self.plot.histosDict.iteritems():
            print compname
            assert(isinstance(comp, Histogram))
            self.pdfs[compname] = RooHistPdf(compname, compname,
                                             RooArgSet(self.xvar),
                                             RooDataHist(compname, compname, RooArgList(self.xvar),
                                                         comp.weighted))
            self.pdfs[compname].Print()
            self.yields[compname] = comp.Integral(xmin=xmin, xmax=xmax)
        pass
            
    def _make_dataset(self):
        pass

    def _fit(self):
        pass

    def draw_pdfs(self):
        self.pframe = self.xvar.frame()
        for pdf in self.pdfs.values():
            pdf.plotOn(self.pframe)
        self.pframe.Draw()
