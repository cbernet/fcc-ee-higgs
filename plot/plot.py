
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

def cut_flow(comp, nevts=sys.maxint, odir=None):
    print comp.name, '-' * 20
    eff = Efficiencies(comp.tree, cuts)
    eff.fill_cut_flow(comp.name, nevts=nevts)
    print eff.str_cut_flow()
    if odir:
        eff.write('{}/cutflow_{}.txt'.format(odir, comp.name))
    
def contamination(self, odir):
    # from cuts_gen_2 import signal_contamination, cut_gen_htautau, cut_gen_hww
    signal_contamination(ZH.tree, cut, odir)

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
    parser.add_option('-g', '--new_cutgen',
                      dest='new_cutgen',
                      action="store_true", default=False, 
                      help="use new ntuple format for cut_gen")
    parser.add_option('-o', '--output',
                      dest='output', default=None)
    parser.add_option('-l', '--lumi',
                      dest='lumi', type=float, default=None)
    options, args = parser.parse_args(sys.argv)
    
    config_fname = args[1]
    
    cfgfile = open(config_fname)
    cfgmod = imp.load_source('config', config_fname, cfgfile)
    globals().update(cfgmod.__dict__)
        
    if options.lumi:
        lumi = options.lumi
    TGaxis.SetMaxDigits(3)
    print channel
    
    odir = None
    if options.output:
        odir = options.output
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
    
    if odir:
        gPad.SaveAs('/'.join([odir, 'stack.png']))

    pdf = PDF(comps)

    if options.cutflow:
        for comp in comps:
            cut_flow(comp, odir=odir)

    fit_canvas = TCanvas("fit_canvas", "fit")
    tfitter = TemplateFitter(plotter.plot)
    fit_canvas.cd()
    tfitter.draw_data()
    tfitter.print_result()
    if odir:
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
        if odir:
            unc_canvas.SaveAs('/'.join([odir, 'uncertainties.png']))
        unc = h.GetMean()
        h.Draw()
        print unc
        if odir:
            unctxtfile = open('/'.join([odir, 'uncertainties.txt']), 'w')
            unctxtfile.write('signal yield uncertainty = {}%'.format(unc))
            unctxtfile.close()
    
    print plotter.plot
    if odir:
        plotter.write('/'.join([odir, 'stack.txt']))
        
    if options.contamination:
        if options.new_cutgen:
            from cuts_gen_2 import signal_contamination, cut_gen_htautau, cut_gen_hww
        else: 
            from cuts_gen import signal_contamination, cut_gen_htautau, cut_gen_hww
        outfile = None
        if odir:
            odir = '/'.join([odir, 'contamination.txt'])
        signal_contamination(ZH.tree, cut, odir)
    
    print 'Results saved in', odir
 
