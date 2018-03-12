if __name__ == '__main__':

    import sys
    import imp
    from cpyroot import *
    from ROOT import TGaxis
    from tdrstyle.tdrstyle import setTDRStyle
    setTDRStyle(square=True)
    
    from fcc_ee_higgs.plot.efficiencies import Efficiencies
            
    config_fname, root_fname = sys.argv[1:]
    
    cfgfile = open(config_fname)
    cfgmod = imp.load_source('config', config_fname, cfgfile)
    locals().update(cfgmod.__dict__)
    
    tfile = TFile(root_fname)
    tree = tfile.Get('events')
    
    c = TCanvas()
