from cpyroot.tools.DataMC import DataMCPlot, Histogram
from ROOT import RooRealVar, RooConstVar, RooDataSet, RooDataHist, RooHistPdf, RooGaussian, RooArgSet, RooAddPdf, RooArgList, RooFit, SetOwnership, RooAbsArg

class Fitter(object):

    def __init__(self, plot):
        assert(isinstance(plot, DataMCPlot))
        self.plot = plot
        self._make_model()
        self._make_dataset()
        self._fit()

    def _make_model(self):
        self.pdfs = {}
        self.yields = {}  # yields are plain floats
        self.ryields = {}  # keep track of roofit objects for memory management
        nbins, xmin, xmax = self.plot.histos[0].GetBinning()
        self.xvar = RooRealVar("x", "x", xmin, xmax)
        self.xvar.setBins(nbins)
        self.pdfs = {}
        self.hists = []
        pdfs = RooArgList()
        yields = RooArgList()
        for compname, comp in self.plot.histosDict.iteritems():
            print compname
            assert(isinstance(comp, Histogram))
            hist = RooDataHist(compname, compname, RooArgList(self.xvar),
                               comp.weighted)
            SetOwnership(hist, False)
            # self.hists.append(hist)
            pdf = RooHistPdf(compname, compname,
                             RooArgSet(self.xvar),
                             hist)
            self.pdfs[compname] = pdf
            self.pdfs[compname].Print()
            pdfs.add(pdf)
            
            nevts = comp.Integral(xmin=xmin, xmax=xmax)
            theyield = RooRealVar('n{}'.format(compname),
                                  'n{}'.format(compname),
                                  nevts,
                                  0, 50000)
            self.ryields[compname] = theyield
            self.yields[compname] = nevts
            yields.add(theyield)
            
        self.model = RooAddPdf('model', 'model',
                               pdfs, yields)
        pass
            
    def _make_dataset(self):
        nevents = sum(self.yields.values())
        self.data = self.model.generate(RooArgSet(self.xvar), nevents)

    def _fit(self):
        tresult = self.model.fitTo(self.data,
                                   RooFit.Extended())

    def draw_pdfs(self):
        self.pframe = self.xvar.frame()
        for pdf in self.pdfs.values():
            pdf.plotOn(self.pframe)
        self.pframe.Draw()
        
    def draw_data(self):
        self.mframe = self.xvar.frame()
        self.data.plotOn(self.mframe)
        self.model.plotOn(self.mframe)
        for icomp, compname in enumerate(self.pdfs):
            self.model.plotOn(self.mframe,
                              RooFit.Components(compname),
                              RooFit.LineColor(icomp+1))
        self.mframe.Draw()
        
