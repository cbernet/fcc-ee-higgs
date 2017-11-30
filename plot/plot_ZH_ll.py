from cpyroot import *

from tdrstyle import tdrstyle
from fcc_ee_higgs.components.ZH_Zmumu import WW, ZZ, ZH
from fcc_ee_higgs.components.tools import load

from fitter import TemplateFitter, BaseFitter, BallFitter
from plotter import Plotter

plot = None

if __name__ == '__main__':
        
    from ROOT import RooRealVar, RooDataHist, RooHistPdf, RooArgList, RooArgSet, TH1

    from fcc_ee_higgs.components.ZH_Zll import ZH, ZZ
    ZH.name =  'ZH'
    ZZ.name =  'ZZ'
    
    # comps = [WW, ZZ, ZH]
    comps = [ZZ, ZH]
    load(comps)
    lumi = 500e12
    # lumi = 5e6  # 5ab-1

    plotter = Plotter(comps, lumi)

    b_wp = (0.75, 0.015)
    # b_wp = (0.6, 3e-3)

    cut_z = '(abs(zeds_m-91)<5. && zeds_pt>10 && zeds_pz<50 && zeds_acol>100 && zeds_cross>10)'    
    cut_rad = '((jets_1_e<0 || jets_1_22_e/jets_1_e<0.8) && \
    (jets_2_e<0 || jets_2_22_e/jets_2_e<0.8))'
    # cut_hbb = '(jets_1_b==1 && jets_2_b==1)'
    cut_hbb = '(((jets_1_bmatch==1 && rndm<{eff}) || (jets_1_bmatch==0 && rndm<{fake})) && \
    ((jets_2_bmatch==1 && rndm<{eff}) || (jets_2_bmatch==0 && rndm<{fake})))'.format(
        eff=b_wp[0], fake=b_wp[1]
    )
    cut_hinv = '(jets_1_e<0 && jets_2_e<0)'
    cut_hvis = '(jets_1_e>0 && jets_2_e>0)'

    cut_ZH = ' && '.join([cut_z, cut_rad, cut_hbb])

    var = 'recoil_m'
    cut = cut_ZH
    bins = 50, 50, 150

    plotter.draw(var, cut, bins)
##    tfitter = TemplateFitter(plotter.plot)
##    tfitter.draw_data()
    
##    for name, pdf in tfitter.pdfs.iteritems():
##        print name, pdf
##        print pdf.Print()
##    tfitter.draw_data()
##    sys.exit(1)
##    fitter.draw_pdfs()

