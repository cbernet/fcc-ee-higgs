
import sys

from cpyroot import *
from ROOT import TGaxis, TFile
from tdrstyle.tdrstyle import setTDRStyle
setTDRStyle(square=True)
from fitter2 import TemplateFitter

hjanik = dict()
rfjanik = TFile("Janik/histos_noscaling.root")
hjanik['ZH'] = rfjanik.Get('HS')
hjanik['ZZ'] = rfjanik.Get('ZZ')
hjanik['ffbar'] = rfjanik.Get('qqbar')

hcolin = dict()
rfcolin = TFile("colin.root")
hcolin['ZH'] = rfcolin.Get('ZH')
hcolin['ZZ'] = rfcolin.Get('ZZ')
hcolin['ffbar'] = rfcolin.Get('ffbar')

weights = dict(
    ZH=(500e3, 200.),
    ZZ=(500e3, 1350.),
    ffbar=(2e6, 52000.)
)

lumi = 5e3

for hname, h in hjanik.iteritems():
    h.SetName(hname)    
    ngen, xsec = weights[hname]
    h.Scale(xsec*lumi/ngen)
     
tfjanik = TemplateFitter(hjanik.values())
tfjanik.draw_data()
tfjanik.print_result()
##
##tfcolin = TemplateFitter(hcolin.values())
##tfcolin.draw_data()
##tfcolin.print_result()

##tfcolin_mod = TemplateFitter([hcolin['ZH'], hcolin['ZZ'], hjanik['ffbar']])
##tfcolin_mod.draw_data()
##tfcolin_mod.print_result()
##
##tfjanik_mod = TemplateFitter([hjanik['ZH'], hjanik['ZZ'], hcolin['ffbar']])
##tfjanik_mod.draw_data()
##tfjanik_mod.print_result()
##
##hjanik['ffbar2'] = hjanik['ffbar'].Clone('ffbar2')
##hjanik['ffbar2'].Scale(72./23.)
##tfjanik_mod2 = TemplateFitter([hjanik['ZH'], hjanik['ZZ'], hjanik['ffbar2']])
##tfjanik_mod2.draw_data()
##tfjanik_mod2.print_result()

##h = TH1F('h', 'uncertainty', 500, 0., 15)
##for i in range(100):
##    tfitter = TemplateFitter(histos)
##    unc = tfitter.print_result()
##    h.Fill(unc)
##c_unc = TCanvas()
##print h.GetMean()
##h.Draw()

