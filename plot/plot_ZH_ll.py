if __name__ == '__main__':

    from cpyroot import *
    from tdrstyle.tdrstyle import setTDRStyle
    setTDRStyle(square=True)
    from fitter import TemplateFitter
    from fcc_ee_higgs.plot.plotter import Plotter
    from fcc_ee_higgs.plot.plotconfig_ZH_ll import comps, var, cut, channel, bins, detector, lumi, xtitle 
            
    do_fit = True

    c = TCanvas()
    plotter = Plotter(comps, lumi)
    plotter.draw(var, cut, bins, title=xtitle)
    plotter.print_info(detector)
    
    gPad.SaveAs('{var}_zh_{channel}_{detector}.png'.format(
        var=var, channel=channel, detector=detector))

    if do_fit:
        tfitter = TemplateFitter(plotter.plot)
        tfitter.draw_data()
        tfitter.print_result()
##    for name, pdf in tfitter.pdfs.iteritems():
##        print name, pdf
##        print pdf.Print()
##    tfitter.draw_data()
##    sys.exit(1)
##    fitter.draw_pdfs()

