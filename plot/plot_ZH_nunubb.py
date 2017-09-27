from cpyroot import *

# from tdrstyle import tdrstyle
from fcc_ee_higgs.components.all import load_components
components = load_components(mode='heppy')
from fitter import TemplateFitter, BaseFitter, BallFitter
from plotter import Plotter
from marginal_efficiency import marginal_efficiency

plot = None

if __name__ == '__main__':
        
    from ROOT import RooRealVar, RooDataHist, RooHistPdf, RooArgList, RooArgSet, TH1
    
    ZZ = components['ee_to_ZZ_Sep12_ZHnunubb_Sep21_A_13']
    ZZ.name = 'ZZ'
    ZH = components['ee_to_ZH_Z_to_nunu_Sep12_ZHnunubb_Sep21_A_12']
    ZH.name =  'ZH'
    ffbar = components['ee_to_ffbar_Sep12_ZHnunubb_Sep21_B_15']
    ffbar.name = 'ffbar'
    
    
    comps = [ZZ, ZH] 
    lumi = 5e5
    # lumi = 5e6  # 5ab-1

    plotter = Plotter(comps, lumi)
    
    cut_missmass= 'misenergy_m>65 && misenergy_m<125'
#     cut_missmass= 'misenergy_m>75 && misenergy_m<150'
    # cut_h_bb = 'jet1_e>0 && jet2_e>0 && (jet1_bmatch==1 && jet2_bmatch==1)'
    cut_h_bb = 'jet1_e>0 && jet2_e>0 && (jet1_b==1 || jet2_b==1)'
    cut_h_pz = 'abs(misenergy_pz)<50'
    cut_h_pt = 'misenergy_pt>15'
    cut_h_acol = 'higgs_acol>100.'
    cut_h_cross = 'higgs_cross>10'
    all_cuts = [cut_missmass, cut_h_bb, cut_h_pz, cut_h_pt, cut_h_acol, cut_h_cross]
    str_all_cuts = ' && '.join(all_cuts)

    var = 'higgs_rescaled_m'
    cut = str_all_cuts
    bins = 50, 50, 150
    
    do_fit = False
    plotter.draw(var, cut, bins)
    if do_fit:
        tfitter = TemplateFitter(plotter.plot)
        tfitter.draw_data()
    
    # marginal_efficiency(ZZ.tree, all_cuts)
##    for name, pdf in tfitter.pdfs.iteritems():
##        print name, pdf
##        print pdf.Print()
##    tfitter.draw_data()
##    sys.exit(1)
##    fitter.draw_pdfs()

