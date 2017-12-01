from cpyroot import *
import sys

from fcc_ee_higgs.plot.plot_ZH_ll import cut_Z

if __name__ == '__main__':
    
    rfile = TFile(sys.argv[1])
    tree = rfile.Get('events')
    tree.Draw('zeds_m', cut_Z)
    print tree.GetSelectedRows()

