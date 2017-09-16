from cpyroot import *

from tdrstyle import tdrstyle
from fcc_ee_higgs.components.all import components
from fitter import TemplateFitter, BaseFitter, BallFitter
from plotter import Plotter

plot = None

if __name__ == '__main__':
        
    from ROOT import RooRealVar, RooDataHist, RooHistPdf, RooArgList, RooArgSet, TH1
    
    ZZ = components['ee_to_ZZ_Sep12_ZHnunubb_1b_A_5']
    ZZ.name = 'ZZ'
    ZH = components['ee_to_ZH_Z_to_nunu_Sep12_ZHnunubb_1b_A_6']
    ZH.name =  'ZH'
    
    comps = [ZZ, ZH] 
    lumi = 1e6
    # lumi = 5e6  # 5ab-1

    plotter = Plotter(comps, lumi)
    
    cut_missingzmass = 'misenergy_m>65 && misenergy_m<125'
    cut_hbb = '(jet1_b==1 && jet2_b==1)'
    cut_haco = 'higgs_pt>10 && higgs_pz<50 && higgs_acol>100 && higgs_cross>10'

    cut_ZHnunubb = '&&'.join([cut_missingzmass, cut_hbb, cut_haco])

    var = 'higgs_m'
    cut = cut_ZHnunubb
    bins = 50, 50, 150

    plotter.draw(var, cut, bins)
    tfitter = TemplateFitter(plotter.plot)
    tfitter.draw_data()
    
##    for name, pdf in tfitter.pdfs.iteritems():
##        print name, pdf
##        print pdf.Print()
##    tfitter.draw_data()
##    sys.exit(1)
##    fitter.draw_pdfs()

