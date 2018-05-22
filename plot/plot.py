import imp
import time
import shutil

from cpyroot import *
from ROOT import TGaxis
from tdrstyle.tdrstyle import setTDRStyle
setTDRStyle(square=True)
from fitter import TemplateFitter
from fcc_ee_higgs.plot.plotter import Plotter
from fcc_ee_higgs.plot.efficiencies import Efficiencies
from fcc_ee_higgs.plot.pdf import PDF

def plot_main(config_fname, options):
    cfgfile = open(config_fname)
    cfgmod = imp.load_source('config', config_fname, cfgfile)
    globals().update(cfgmod.__dict__)
        
    TGaxis.SetMaxDigits(3)
    print channel
    
    odir = None
    if options.output:
        odir = options.output
    else:
        odir = '{var}_zh_{channel}_{detector}_{time}'.format(
            var=var, channel=channel, detector=detector,
            time=time.strftime("%Y%m%d-%H%M%S", time.localtime())
        )
    if os.path.isdir(odir):
        answer = None
        while answer not in ['y', 'n']:
            answer = raw_input('remove directory {}?'.format(odir))
            if answer == 'y':
                shutil.rmtree(odir)
                break
            elif answer == 'n':
                sys.exit(1)
    os.mkdir(odir)

    c = TCanvas()
    plotter = Plotter(comps, lumi)
    nbins, xmin, xmax = bins
    gevperbin = int((xmax - xmin) / nbins)
    plotter.draw(var, cut, bins, xtitle=xtitle, ytitle='Events/{} GeV'.format(gevperbin))
    plotter.print_info(detector)
    
    gPad.SaveAs('/'.join([odir, 'stack.png']))

    pdf = PDF(comps)

    if options.cutflow:
        effs = {}
        for comp in comps:
            print comp.name, '-' * 20
            effs[comp.name] = Efficiencies(comp.tree, cuts)
            eff = effs[comp.name]
            eff.fill_cut_flow(comp.name)
            print eff.str_cut_flow()
            eff.write('{}/cutflow_{}.txt'.format(odir, comp.name))
            # eff.marginal()

    fit_canvas = TCanvas("fit_canvas", "fit")
    tfitter = TemplateFitter(plotter.plot)
    fit_canvas.cd()
    tfitter.draw_data()
    tfitter.print_result()
    fit_canvas.SaveAs('/'.join([odir, 'fit.png']))

    unc_canvas = None
    if options.fit:
        unc_canvas = TCanvas('unc_canvas', 'uncertainty')
        h = TH1F('h', 'uncertainty', 500, 0., 15)
        for i in range(100):
            tmpfitter = TemplateFitter(plotter.plot)
            unc = tmpfitter.print_result()
            h.Fill(unc)
        h.Draw()
        unc_canvas.SaveAs('/'.join([odir, 'uncertainties.png']))
        unc = h.GetMean()
        h.Draw()
        print unc
        unctxtfile = open('/'.join([odir, 'uncertainties.txt']), 'w')
        unctxtfile.write('signal yield uncertainty = {}%'.format(unc))
        unctxtfile.close()
    
    print plotter.plot
    plotter.write('/'.join([odir, 'stack.txt']))
        
    if options.contamination:
        from cuts_gen import signal_contamination, cut_gen_htautau, cut_gen_hww
        signal_contamination(ZH.tree, cut, '/'.join([odir, 'contamination.txt']))
    

if __name__ == '__main__':

    import sys
    from optparse import OptionParser
    
    parser = OptionParser()
    parser.usage = """plot.py <plotconfig file>
    do the stack plot.
    """
    parser.add_option('-n', '--nothing',
                      dest='nothing',
                      action="store_true", default=False, 
                      help="just load the components and do nothing")
    parser.add_option('-f', '--fit',
                      dest='fit',
                      action="store_true", default=False, 
                      help="perform the template fit")
    parser.add_option('-c', '--cutflow',
                      dest='cutflow',
                      action="store_true", default=False, 
                      help="show the cutflow")
    parser.add_option('-s', '--contamination',
                      dest='contamination',
                      action="store_true", default=False, 
                      help="show the signal contamination")
    parser.add_option('-o', '--output',
                      dest='output', default=None)
    options, args = parser.parse_args(sys.argv)
    
    config_fname = args[1]
    
    plot_main(config_fname, options)
    
 
