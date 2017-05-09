from cpyroot import *
from cpyroot.tools.style import * 
from cpyroot.tools.DataMC.DataMCPlot import DataMCPlot

histPref = {
    'ZZ*': {'style':sHTT_VV, 'layer':10, 'legend':'ZZ'},
    'WW*': {'style':sHTT_WJets, 'layer':5, 'legend':'WW'},
    'ZH*': {'style':sHTT_Higgs, 'layer':1001, 'legend':'ZH'},
}

def load(comp, basedir):
    comp.directory = '/'.join([basedir, comp.name])
    print comp.directory
    comp.rootfile = TFile('{}/{}'.format(
        comp.directory,
        'heppy.analyzers.examples.zh.ZHTreeProducer.ZHTreeProducer_1/tree.root'
    ))
    comp.tree = comp.rootfile.Get('events')
    
def project(comp, var, cut, *bins):
    hist_name = '{} : {} | {}'.format(comp.name, var, cut)
    hist = TH1F(hist_name, '', *bins)
    comp.tree.Project(hist.GetName(), var, cut)
    print hist_name
    return hist

if __name__ == '__main__':
    from fcc_ee_higgs.components.ZH_Zmumu import WW, ZZ, ZH_Zmumu
    
    basedir = '/Users/cbernet/Code/FCC/fcc_ee_higgs/samples/ana/Prod2'
    load(WW, basedir)
    load(ZZ, basedir)
    load(ZH_Zmumu, basedir)
    
    print ZZ
    
    var = 'recoil_m'
    cut = 'zed_m>50'
    bins = 50, 50, 150
    hist_ZZ = project(ZZ, var, cut, *bins)
    hist_ZH_Zmumu = project(ZH_Zmumu, var, cut, *bins)
    
    plot = DataMCPlot('recoil', histPref)
    plot.AddHistogram('ZH_Zmumu', hist_ZH_Zmumu)
    plot.AddHistogram('ZZ', hist_ZZ)
    lumi = 5e6  # 5ab-1
    plot.histosDict['ZH_Zmumu'].SetWeight(ZH_Zmumu.getWeight(lumi).GetWeight())
    plot.histosDict['ZZ'].SetWeight(ZZ.getWeight(lumi).GetWeight())
    plot.DrawStack()
    

    
