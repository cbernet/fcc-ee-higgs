if __name__ == '__main__':

    from cpyroot import *
    from ROOT import TGaxis
    from tdrstyle.tdrstyle import setTDRStyle
    setTDRStyle(square=True)
    from fitter import TemplateFitter
    from fcc_ee_higgs.plot.plotter import Plotter
    from fcc_ee_higgs.plot.plotconfig_ZH_ll import comps, var, cut, channel, bins, detector, lumi, xtitle 
            
    do_fit = True

    TGaxis.SetMaxDigits(3)

    c = TCanvas()
    plotter = Plotter(comps, lumi)
    nbins, xmin, xmax = bins
    gevperbin = int((xmax - xmin) / nbins)
    plotter.draw(var, cut, bins, xtitle=xtitle, ytitle='Events/{} GeV'.format(gevperbin))
    # plotter.print_info(detector)
    plotter.print_info("")
    
    gPad.SaveAs('{var}_zh_{channel}_{detector}.png'.format(
        var=var, channel=channel, detector=detector))

    if do_fit:
        tfitter = TemplateFitter(plotter.plot)
        tfitter.draw_data()
        tfitter.print_result()

