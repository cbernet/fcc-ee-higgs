from cpyroot import *
from cpyroot.tools.style import * 
from cpyroot.tools.DataMC.DataMCPlot import DataMCPlot

histPref = {
    'ZZ*': {'style':sBlue, 'layer':10, 'legend':'ZZ'},
    'WW*': {'style':sRed, 'layer':5, 'legend':'WW'},
    'ZH*': {'style':sGreen, 'layer':1001, 'legend':'ZH'},
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
    # hist_name = '{} : {} | {}'.format(comp.name, var, cut)
    hist_name = comp.name
    hist = TH1F(hist_name, '', *bins)
    comp.tree.Project(hist.GetName(), var, cut)
    print hist_name
    return hist

if __name__ == '__main__':

    from tdrstyle import tdrstyle
    from fcc_ee_higgs.components.ZH_Zmumu import WW, ZZ, ZH
    
    basedir = '/Users/cbernet/Code/FCC/fcc_ee_higgs/samples/ana/May16'
    load(WW, basedir)
    load(ZZ, basedir)
    load(ZH, basedir)
    
    print ZZ
    
    var = 'recoil_m'
    cut = 'abs(zed_m-91)<5. && zed_pt>10 && zed_pz<50 && zed_acol>100 && zed_acop>10 && (jet1_e<0 || jet1_22_e/jet1_e<0.8) && (jet2_e<0 || jet2_22_e/jet2_e<0.8)'
    # cut = 'zed_m>50'
    bins = 100, 50, 150
    
    lumi = 5e6  # 5ab-1
    lumi = 1000e3
    
    samples = [WW, ZZ, ZH]
    plot = DataMCPlot('recoil', histPref)
    for sample in samples:
        hist = project(sample, var, cut, *bins)    
        plot.AddHistogram(sample.name, hist)
        plot.histosDict[sample.name].SetWeight(sample.getWeight(lumi).GetWeight())
    plot.legendBorders = (0.22, 0.65, 0.44, 0.92)
    plot.DrawStack()
    # plot.histosDict['ZH'].Draw()
    plot.supportHist.GetYaxis().SetRangeUser(0,2300)
    plot.supportHist.GetYaxis().SetTitleOffset(1.35)
    plot.supportHist.GetYaxis().SetNdivisions(5)
    plot.supportHist.GetXaxis().SetNdivisions(5)
    plot.supportHist.GetXaxis().SetTitle("recoil mass (GeV)")
    gPad.Modified()
    gPad.Update()
    
    
