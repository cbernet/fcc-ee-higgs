from cpyroot import *

from tdrstyle import tdrstyle
from fcc_ee_higgs.components.ZH_Zmumu import WW, ZZ, ZH
from fitter import TemplateFitter, BaseFitter, BallFitter
from plotter import Plotter

plot = None

if __name__ == '__main__':
        
    from ROOT import RooRealVar, RooDataHist, RooHistPdf, RooArgList, RooArgSet, TH1

    basedir = '/Users/cbernet/Code/FCC/fcc_ee_higgs/samples/analysis/ZH_ll/June12'
    comps = [WW, ZZ, ZH] 
    lumi = 1e6
    # lumi = 5e6  # 5ab-1

    plotter = Plotter(basedir, comps, lumi)

    cut = 'abs(zed_m-91)<5. && zed_pt>10 && zed_pz<50 && zed_acol>100 && zed_acop>10 \
    && (jet1_e<0 || jet1_22_e/jet1_e<0.8) && (jet2_e<0 || jet2_22_e/jet2_e<0.8) && (jet1_b==1 || jet2_b==1)'

    cut_z = '(abs(zed_m-91)<5. && zed_pt>10 && zed_pz<50 && zed_acol>100 && zed_acop>10'
    
    cut_rad = '(jet1_e<0 || jet1_22_e/jet1_e<0.8) && (jet2_e<0 || jet2_22_e/jet2_e<0.8))'
    cut_hbb = '(jet1_b==1 || jet2_b==1)'
    cut_hinv = '(jet1_e<0 && jet2_e<0)'
    cut_hvis = 'jet1_e>0 && jet2_e>0'

    cut_ZH = ' && '.join([cut_z, cut_rad])

    var = 'recoil_m'
    cut = cut_ZH
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

