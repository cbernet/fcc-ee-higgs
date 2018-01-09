from cpyroot import *

from tdrstyle import tdrstyle
# from fcc_ee_higgs.components.ZH_nunubb import ZH, ZZ, ffbar
from fcc_ee_higgs.components.tools import load

from fitter import TemplateFitter, BaseFitter, BallFitter
from fcc_ee_higgs.plot.plotter import Plotter
from marginal_efficiency import marginal_efficiency

plot = None

if __name__ == '__main__':
    from ROOT import RooRealVar, RooDataHist, RooHistPdf, RooArgList, RooArgSet, TH1
        
    detector = 'cms'
    plot_missmass = False
    bb_operator = ' || '
    if detector is 'cms':
        from fcc_ee_higgs.components.ZH_nunubb import ZH, ZZ, WW, ffbar
    elif detector is 'clic':
        from fcc_ee_higgs.components.ZH_nunubb_clic import ZH, ZZ, ffbar
    ZH.name =  'ZH' 
    ZZ.name =  'ZZ'
    WW.name = 'WW'
    ffbar.name =  'ffbar'    
    comps = [ZZ, ZH, WW]
    load(comps)
    lumi = 500e12
    # lumi = 5e6  # 5ab-1
    
    # cut_missmass= 'missing_energy_m>65 && missing_energy_m<125'
    cut_missmass= 'missing_energy_m>80 && missing_energy_m<125'  # reoptimized cut
    from fcc_ee_higgs.plot.plot_ZH_ll import get_cut_hbb, b_wp
    if detector is 'clic':
        b_wp = (0.8, 4e-3)
    cut_hbb = get_cut_hbb(b_wp[0], b_wp[1], bb_operator)
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
    label = 'PAPAS (CMS)'
    if detector is 'clic':
        label = 'PAPAS (CLIC-FCCee)'
    
    
    if plot_missmass:
        comps = [ZH, ZZ, WW, ffbar]
        var = 'missing_energy_m'
        cuts = [cut_h_pz, cut_h_pt, cut_h_acol, cut_h_cross, cut_hbb]
        cut = ' && '.join(cuts)
        title = 'Missing mass (GeV)'
        bins = 50, 0, 200
    
    plotter = Plotter(comps, lumi)
        
    do_fit = False
    c = TCanvas()
    plotter.draw(var, cut, bins, title=title, label=label)
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

