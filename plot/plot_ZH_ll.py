from cpyroot import *

from tdrstyle.tdrstyle import setTDRStyle
setTDRStyle(square=False)
from fcc_ee_higgs.components.tools import load

from fitter import TemplateFitter, BaseFitter, BallFitter
from fcc_ee_higgs.plot.plotter import Plotter

import pprint

plot = None

#b_wp = (0.6, 0.01)
lep_eff = 0.95
b_wp = (0.6, 3e-3)

cut_leps = '(zeds_1_iso_e/zeds_1_e<0.2) && (zeds_1_iso_e/zeds_1_e<0.2) && zeds_1_e>0 && zeds_2_e>0'
cut_z = '(abs(zeds_m-91)<4. && zeds_pt>10 && zeds_pz<50 && zeds_acol>100 && zeds_cross>10) && (zeds_1_pdgid==-zeds_2_pdgid) '
cut_eff_z = '(rndm<{lep_eff} && rndm<{lep_eff} && zeds_1_pt>7 && zeds_2_pt>7)'.format(lep_eff=lep_eff)
cut_rad = '((jets_1_e<0 || jets_1_22_e/jets_1_e<0.8) && \
(jets_2_e<0 || jets_2_22_e/jets_2_e<0.8))'
# cut_hbb = '(jets_1_b==1 && jets_2_b==1)'
cut_hbb = '(((jets_1_bmatch==1 && rndm<{eff}) || (jets_1_bmatch==0 && rndm<{fake})) || \
((jets_2_bmatch==1 && rndm<{eff}) || (jets_2_bmatch==0 && rndm<{fake})))'.format(
    eff=b_wp[0], fake=b_wp[1]
)
cut_hinv = '(jets_1_e<0 && jets_2_e<0)'
cut_hvis = '(jets_1_e>0 && jets_2_e>0)'

cut_Z = ' && '.join([cut_leps, cut_z, cut_rad, cut_hbb])


if __name__ == '__main__':
        
    from ROOT import RooRealVar, RooDataHist, RooHistPdf, RooArgList, RooArgSet, TH1

    from fcc_ee_higgs.components.ZH_Zll import ZH, ZZ, WW
    ZH.name =  'ZH'
    ZZ.name =  'ZZ'
    WW.name =  'WW'
    
    # comps = [WW, ZZ, ZH]
    comps = [WW, ZZ, ZH]
    load(comps)
    lumi = 500e12
    # lumi = 5e6  # 5ab-1

    plotter = Plotter(comps, lumi)

    var = 'recoil_m'
    cut = cut_Z 
    bins = 50, 50, 150

    plotter.draw(var, cut, bins, title='Higgs mass (GeV)')
##    tfitter = TemplateFitter(plotter.plot)
##    tfitter.draw_data()
    
##    for name, pdf in tfitter.pdfs.iteritems():
##        print name, pdf
##        print pdf.Print()
##    tfitter.draw_data()
##    sys.exit(1)
##    fitter.draw_pdfs()

