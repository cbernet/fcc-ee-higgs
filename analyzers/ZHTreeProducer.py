from heppy.framework.analyzer import Analyzer
from heppy.statistics.tree import Tree
from fcc_ee_higgs.analyzers.ntuple import *

from ROOT import TFile

class ZHTreeProducer(Analyzer):

    def beginLoop(self, setup):
        super(ZHTreeProducer, self).beginLoop(setup)
        self.rootfile = TFile('/'.join([self.dirName,
                                        'tree.root']),
                              'recreate')
        self.tree = Tree( 'events', '')
        if hasattr(self.cfg_ana, 'recoil'):
            bookParticle(self.tree, 'recoil')
        if hasattr(self.cfg_ana, 'zeds'):  
            bookZed(self.tree, 'zed')
        self.taggers = ['b', 'bmatch', 'bfrac']
        bookJet(self.tree, 'jet1', self.taggers)
        bookJet(self.tree, 'jet2', self.taggers)
        bookJet(self.tree, 'jet1_rescaled', self.taggers)
        bookJet(self.tree, 'jet2_rescaled', self.taggers)
        for label in self.cfg_ana.higgs:
            bookResonanceWithLegs(self.tree, label)
##        bookResonanceWithLegs(self.tree, 'genb1')
##        bookResonanceWithLegs(self.tree, 'genb2')
        for label in self.cfg_ana.misenergy:
            bookParticle(self.tree, label)
        var(self.tree, 'n_nu')
       
    def process(self, event):
        self.tree.reset()
        if hasattr(self.cfg_ana, 'recoil'):
            recoil = getattr(event, self.cfg_ana.recoil)    
            fillParticle(self.tree, 'recoil', recoil)
        if hasattr(self.cfg_ana, 'zeds'):  
            zeds = getattr(event, self.cfg_ana.zeds)
            if len(zeds)>0:
                zed = zeds[0]
                fillZed(self.tree, 'zed', zed)
        for label in self.cfg_ana.misenergy:        
            misenergy = getattr(event, label)
            fillParticle(self.tree, label, misenergy)      
        jets = getattr(event, self.cfg_ana.jets)
        for ijet, jet in enumerate(jets):
            if ijet == 2:
                break
            fillJet(self.tree, 'jet{ijet}'.format(ijet=ijet+1), jet, self.taggers)
        jets_rescaled = getattr(event, self.cfg_ana.jets_rescaled)
        for ijet, jet in enumerate(jets_rescaled):
            if ijet == 2:
                break
            fillJet(self.tree, 'jet{ijet}_rescaled'.format(ijet=ijet+1), jet, self.taggers)
        for label in self.cfg_ana.higgs:
            higgses = getattr(event, label)
            if len(higgses)>0:  
                higgs = higgses[0]
                fillResonanceWithLegs(self.tree, label, higgs)
        neutrinos = getattr(event, 'neutrinos', None)
        if neutrinos:
            fill(self.tree, 'n_nu', len(neutrinos))
##        for i, boson in enumerate(event.gen_bosons):
##            if i == 2:
##                break
##            fillResonanceWithLegs(self.tree, 'genb{i}'.format(i=i+1), boson)            
        self.tree.tree.Fill()
        
    def write(self, setup):
        self.rootfile.Write()
        self.rootfile.Close()
        
