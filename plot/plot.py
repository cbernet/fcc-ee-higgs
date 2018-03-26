if __name__ == '__main__':

    import sys
    import imp
    from optparse import OptionParser
    
    from cpyroot import *
    from ROOT import TGaxis
    from tdrstyle.tdrstyle import setTDRStyle
    setTDRStyle(square=True)
    from fitter import TemplateFitter
    from fcc_ee_higgs.plot.plotter import Plotter
    from fcc_ee_higgs.plot.efficiencies import Efficiencies
    from fcc_ee_higgs.plot.pdf import PDF

    parser = OptionParser()
    parser.usage = """plot.py <plotconfig file>
    do the stack plot.
    """
    parser.add_option('-f', '--fit',
                      dest='fit',
                      action="store_true", default=False, 
                      help="perform the template fit")
    parser.add_option('-c', '--cutflow',
                      dest='cutflow',
                      action="store_true", default=False, 
                      help="show the cutflow")
    options, args = parser.parse_args(sys.argv)
    
    config_fname = args[1]
    cfgfile = open(config_fname)
    cfgmod = imp.load_source('config', config_fname, cfgfile)
    locals().update(cfgmod.__dict__)
        
    TGaxis.SetMaxDigits(3)

    c = TCanvas()
    plotter = Plotter(comps, lumi)
    nbins, xmin, xmax = bins
    gevperbin = int((xmax - xmin) / nbins)
    plotter.draw(var, cut, bins, xtitle=xtitle, ytitle='Events/{} GeV'.format(gevperbin))
    plotter.print_info(detector)
    
    gPad.SaveAs('{var}_zh_{channel}_{detector}.png'.format(
        var=var, channel=channel, detector=detector))

    pdf = PDF(comps)

    if options.cutflow:
        effs = {}
        for comp in comps:
            print comp.name, '-' * 20
            effs[comp.name] = Efficiencies(comp.tree, cuts)
            eff = effs[comp.name]
            eff.fill_cut_flow(comp.name)
            eff.print_cut_flow()
            eff.marginal()

    if options.fit:
        tfitter = TemplateFitter(plotter.plot)
        tfitter.draw_data()
        tfitter.print_result()

        h = TH1F('h', 'uncertainty', 500, 0., 15)
        for i in range(100):
            tfitter = TemplateFitter(plotter.plot)
            unc = tfitter.print_result()
            h.Fill(unc)
        c_unc = TCanvas()
        print h.GetMean()
        h.Draw()

    from cuts_gen import signal_contamination, cut_gen_htautau, cut_gen_hww
    signal_contamination(ZH.tree, cut)
