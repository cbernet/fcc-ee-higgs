
import sys

from cpyroot import *
from ROOT import TGaxis, TFile
from tdrstyle.tdrstyle import setTDRStyle
setTDRStyle(square=True)
from fitter2 import TemplateFitter

cut = "zzMin>10&&wwMin>10&&ZMass>82.&&chi2<15"

samples = dict(
    ZH='Patrick/FJ/Higgs.root',
    qqbar='Patrick/FJ/QQ.root',
    WW='Patrick/FJ/WW.root',
    ZZ='Patrick/FJ/ZZ.root',    
)

class Sample(object):
    def __init__(self, name, fname):
        self.name = name
        self.fname = fname
        self.rootfile = TFile(fname)
        self.tree = self.rootfile.Get("FourJetTreeProducer_FourJetAnalyzer")
        self.hist = TH1F(self.name, self.name, 50, 100.5, 150.5)
        self.tree.Project(self.hist.GetName(), 'ZMass+HMass-91.',
                          "zzMin>10&&wwMin>10&&ZMass>82.&&chi2<15")

comps = dict()
 
for sname, fname in samples.iteritems():
    comps[sname] = Sample(sname, fname)

comps['ZH'].hist.Scale(1.03)
comps['ZZ'].hist.Scale(0.65)
comps['WW'].hist.Scale(4.)
comps['qqbar'].hist.Scale(4.0)

##weights = dict(
##    ZH=(500e3, 200.),
##    ZZ=(500e3, 1350.),
##    qqbar=(2e6, 52000.)
##)
##
##lumi = 5e3
##
##for hname, h in histos.iteritems():
##    h.SetName(hname)
##    ngen, xsec = weights[hname]
##    h.Scale(xsec*lumi/ngen)
##

histos = [sample.hist for sample in comps.values()]

for h in histos:
     h.Scale(10.)

tfitter = TemplateFitter(histos)
tfitter.draw_data()
tfitter.print_result()

h = TH1F('h', 'uncertainty', 500, 0., 15)
for i in range(100):
    tfitter = TemplateFitter(histos)
    unc = tfitter.print_result()
    h.Fill(unc)
c_unc = TCanvas()
print h.GetMean()
h.Draw()

