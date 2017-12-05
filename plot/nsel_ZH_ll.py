from cpyroot import *
import sys

from fcc_ee_higgs.plot.plot_ZH_ll import cut_Z, cut_leps

colors = range(1, 5)

def efficiency(cutstr, opt=''):
    print cutstr
    tree.SetLineColor(colors.pop())
    tree.Draw('zeds_m', cutstr, opt)
    nsel = tree.GetSelectedRows()
    print 'n_sel:', nsel
    print 'eff  :', nsel / float(ntot) 
    

if __name__ == '__main__':
    
    dataset = sys.argv[1]
    rfname = '/'.join([dataset, 'fcc_ee_higgs.analyzers.ZHTreeProducer.ZHTreeProducer_1/tree.root'])
    sfname = '/'.join([dataset, 'software.yaml'])
    rfile = TFile(rfname)
    tree = rfile.Get('events')
    ntot = tree.GetEntries()
    print sys.argv[1]
    print 'n_tot:', ntot
    with open(sfname) as soft:
        print soft.read()
    
    efficiency(cut_leps )
    
    efficiency(cut_Z, 'same')
