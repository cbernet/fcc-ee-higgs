from cpyroot import *
import sys

from fcc_ee_higgs.plot.plot_ZH_ll import cut_Z

if __name__ == '__main__':
    
    dataset = sys.argv[1]
    rfname = '/'.join([dataset, 'fcc_ee_higgs.analyzers.ZHTreeProducer.ZHTreeProducer_1/tree.root'])
    sfname = '/'.join([dataset, 'software.yaml'])
    rfile = TFile(rfname)
    tree = rfile.Get('events')
    tree.Draw('zeds_m', cut_Z, 'goff')
    print sys.argv[1]
    print tree.GetSelectedRows()
    with open(sfname) as soft:
        print soft.read()

