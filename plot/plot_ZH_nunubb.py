from cpyroot import *

from tdrstyle import tdrstyle
from fcc_ee_higgs.components.ZH_Znunu import ZHnunu, ZZ, ffbar
from fcc_ee_higgs.components.tools import load

from fitter import TemplateFitter, BaseFitter, BallFitter
from fcc_ee_higgs.plot.plotter import Plotter
from marginal_efficiency import marginal_efficiency

plot = None

if __name__ == '__main__':
        
    from ROOT import RooRealVar, RooDataHist, RooHistPdf, RooArgList, RooArgSet, TH1
    ZHnunu.name =  'ZH'
    ZZ.name =  'ZZ'
    ffbar.name =  'ffbar'
##    ffbar = components['ee_to_ffbar_Sep12_ZHnunubb_Sep21_B_15']
##    ffbar.name = 'ffbar'
    
    
    comps = [ZZ, ZHnunu, ffbar]
    load(comps)
    lumi = 500e12
    # lumi = 5e6  # 5ab-1
    
    # cut_missmass= 'missing_energy_m>65 && missing_energy_m<125'
    cut_missmass= 'missing_energy_m>80 && missing_energy_m<135'
    # cut_h_bb = 'jet1_e>0 && jet2_e>0 && (jet1_bmatch==1 && jet2_bmatch==1)'
    from fcc_ee_higgs.plot.plot_ZH_ll import cut_hbb
    cut_hbb = cut_hbb.replace('jets_1', 'jet1')
    cut_hbb = cut_hbb.replace('jets_2', 'jet2')
    # cut_h_bb = 'jet1_e>0 && jet2_e>0 && (jet1_b==1 && jet2_b==1)'
    cut_h_pz = 'abs(missing_energy_pz)<50'
    cut_h_pt = 'missing_energy_pt>15'
    cut_h_acol = 'higgses_acol>100.'
    cut_h_cross = 'higgses_cross>10'
    all_cuts = [cut_missmass, cut_hbb, cut_h_pz, cut_h_pt, cut_h_acol, cut_h_cross]
    str_all_cuts = ' && '.join(all_cuts)

    var = 'higgses_rescaled_m'
    cut = str_all_cuts
    bins = 50, 50, 150
    title = 'Higgs mass (GeV)' 
    
    plot_missmass = False
    if plot_missmass:
        comps = [ZHnunu, ZZ]
        var = 'missing_energy_m'
        cuts = [cut_h_pz, cut_h_pt, cut_h_acol, cut_h_cross]
        cut = ' && '.join(cuts)
        title = 'Missing mass (GeV)'
        bins = 50, 0, 200
    
    plotter = Plotter(comps, lumi)
        
    do_fit = False
    c = TCanvas()
    plotter.draw(var, cut, bins, title=title)
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

