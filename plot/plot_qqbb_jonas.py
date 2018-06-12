
import sys

from cpyroot import *
from ROOT import TGaxis, TFile
TGaxis.SetMaxDigits(3)
from tdrstyle.tdrstyle import setTDRStyle
setTDRStyle(square=True)
from fcc_ee_higgs.plot.fitter2 import TemplateFitter
from fcc_ee_higgs.plot.histplotter import HistPlotter

rootfile = TFile('Jonas/CLD_fourjet.root')

ZH = rootfile.Get('ZH')
ZH.SetName('ZH')
WW = rootfile.Get('WW')
WW.SetName('WW')
ZZ = rootfile.Get('ZZ')
ZZ.SetName('ZZ')
qqbar = rootfile.Get('qqbar')
qqbar.SetName('qqbar')

histos = [ZH, WW, ZZ, qqbar]

for h in histos:
     lsize = 0.05
     tsize = 0.06
     h.GetXaxis().SetLabelSize(lsize)
     h.GetXaxis().SetTitleSize(tsize)
     h.GetYaxis().SetLabelSize(lsize)
     h.GetYaxis().SetTitleSize(tsize)
##for h in histos:
##     h.Scale(0.1)
lumi = 5000e12

c = TCanvas()
plotter = HistPlotter(histos, lumi)
plotter.draw('m_{miss}', 'Events/1 GeV')
plotter.print_info('CLD')

gPad.SaveAs(rootfile.GetName().replace('.root', '.png'))
##fit_canvas = TCanvas("fit_canvas", "fit")
##tfitter = TemplateFitter(histos)
##tfitter.draw_data()
##tfitter.print_result()
##
##h = TH1F('h', 'uncertainty', 500, 0., 15)
##for i in range(100):
##    tfitter = TemplateFitter(histos)
##    unc = tfitter.print_result()
##    h.Fill(unc)
##c_unc = TCanvas()
##print h.GetMean()
##h.Draw()
##
