
import sys

from cpyroot import *
from ROOT import TGaxis, TFile
from tdrstyle.tdrstyle import setTDRStyle
setTDRStyle(square=True)
from fitter2 import TemplateFitter

rootfile = TFile("Janik/histos_noscaling.root")


histos = dict()
histos['ZH'] = rootfile.Get('HS')
histos['ZZ'] = rootfile.Get('ZZ')
histos['qqbar'] = rootfile.Get('qqbar')

weights = dict(
    ZH=(500e3, 200.),
    ZZ=(500e3, 1350.),
    qqbar=(2e6, 52000.)
)

lumi = 5e3

for hname, h in histos.iteritems():
    h.SetName(hname)
    ngen, xsec = weights[hname]
    h.Scale(xsec*lumi/ngen)
    
tfitter = TemplateFitter(histos.values())
tfitter.draw_data()
tfitter.print_result()

##h = TH1F('h', 'uncertainty', 500, 0., 15)
##for i in range(100):
##    tfitter = TemplateFitter(histos)
##    unc = tfitter.print_result()
##    h.Fill(unc)
##c_unc = TCanvas()
##print h.GetMean()
##h.Draw()

