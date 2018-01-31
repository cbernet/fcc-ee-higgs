from cpyroot import *

from tdrstyle.tdrstyle import setTDRStyle
setTDRStyle(square=True)
from fcc_ee_higgs.components.tools import load

from fitter import TemplateFitter, BaseFitter, BallFitter
from fcc_ee_higgs.plot.plotter import Plotter

import pprint

plot = None

from ROOT import TPaveText
infos = []
def print_info(detector, lumimb):
    lumi = int(lumimb/1e12)  # now in fb-1
    xmin, ymin = 0.62, 0.7
    xmax, ymax = xmin + 0.288, ymin + 0.15
    pave = TPaveText(xmin, ymin, xmax, ymax, 'ndc')
    pave.AddText(detector)
    pave.AddText('{lumi} fb^{{-1}}'.format(lumi=lumi))
    pave.SetTextSizePixels(28)
    pave.SetTextAlign(11)
    pave.SetBorderSize(0)
    pave.SetFillColor(0)
    pave.SetFillStyle(0)
    pave.Draw()
    infos.append(pave)
    
def get_cut_hbb(eff, fake, operator='||'):
    return '(((jets_1_bmatch==1 && rndm<{eff}) || (jets_1_bmatch==0 && rndm<{fake})) {op} \
((jets_2_bmatch==1 && rndm<{eff}) || (jets_2_bmatch==0 && rndm<{fake})))'.format(eff=eff, fake=fake, op=operator)
        
detector = 'cms'
if detector is 'cms':
    from fcc_ee_higgs.components.ZH_Zll import ZH, ZZ, WW
    b_wp = (0.6, 3e-3)    
elif detector is 'clic':
    from fcc_ee_higgs.components.ZH_Zll_clic import ZH, ZZ, WW
    b_wp = (0.8, 4e-3)
comps = [ZZ, ZH, WW]
ZH.name =  'ZH'
ZZ.name =  'ZZ'
WW.name =  'WW'
    
# lep_eff = 0.95
# b_wp = (0.6, 3e-3)
# b_wp = (0.7, 1.7e-2)

cut_leps = '(zeds_1_iso_e/zeds_1_e<0.2) && (zeds_1_iso_e/zeds_1_e<0.2) && zeds_1_e>0 && zeds_2_e>0'
cut_z = '(abs(zeds_m-91)<4. && zeds_pt>10 && zeds_pz<50 && zeds_acol>100 && zeds_cross>10) && (zeds_1_pdgid==-zeds_2_pdgid) '
# cut_eff_z = '(rndm<{lep_eff} && rndm<{lep_eff} && zeds_1_pt>7 && zeds_2_pt>7)'.format(lep_eff=lep_eff)
cut_rad = '((jets_1_e<0 || jets_1_22_e/jets_1_e<0.8) && \
(jets_2_e<0 || jets_2_22_e/jets_2_e<0.8))'
# cut_hbb = '(jets_1_b==1 && jets_2_b==1)'
cut_hbb = get_cut_hbb(b_wp[0], b_wp[1], ' || ')
cut_hinv = '(jets_1_e<0 && jets_2_e<0)'
cut_hvis = '(jets_1_e>0 && jets_2_e>0)'

cut_Z = ' && '.join([cut_leps, cut_z, cut_rad])


if __name__ == '__main__':
        
    from ROOT import RooRealVar, RooDataHist, RooHistPdf, RooArgList, RooArgSet, TH1
    
    do_fit = False
    load(comps)
    lumi = 500e12
    # channel = 'inclusive'
    channel = 'inclusive'
    cut = cut_Z
    if channel is 'bb':
        cut = ' && '.join([cut_Z, cut_hbb])
    # lumi = 5e6  # 5ab-1

    plotter = Plotter(comps, lumi)

    var = 'recoil_m'
    bins = 50, 50, 150


    plotter.draw(var, cut, bins, title='m_{H} (GeV)')
    
    label = 'PAPAS\n(CMS)'
    if detector is 'clic':
        label = 'PAPAS\n(CLIC-FCCee)'
    latex = TLatex()
    latex.DrawLatexNDC(0.50, 0.88, label)
    
    gPad.SaveAs('{var}_zh_{channel}_{detector}.png'.format(
        var=var, channel=channel, detector=detector))

    if do_fit:
        tfitter = TemplateFitter(plotter.plot)
        tfitter.draw_data()
        tfitter.tresult.Print()
    
##    for name, pdf in tfitter.pdfs.iteritems():
##        print name, pdf
##        print pdf.Print()
##    tfitter.draw_data()
##    sys.exit(1)
##    fitter.draw_pdfs()

