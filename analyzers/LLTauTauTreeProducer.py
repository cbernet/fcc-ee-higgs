from heppy.framework.analyzer import Analyzer
from heppy.statistics.tree import Tree
from fcc_ee_higgs.analyzers.ntuple import *

from ROOT import TFile

class LLTauTauTreeProducer(Analyzer):

    def beginLoop(self, setup):
        super(LLTauTauTreeProducer, self).beginLoop(setup)
        self.rootfile = TFile('/'.join([self.dirName,
                                        'tree.root']),
                              'recreate')
        self.tree = Tree( 'events', '')
        if hasattr(self.cfg_ana, 'recoil'):
            bookParticle(self.tree, 'recoil')
        if hasattr(self.cfg_ana, 'zeds'):  
            bookZed(self.tree, 'zed')
        self.taggers = ['b', 'bmatch', 'bfrac']
        for label in self.cfg_ana.particles:
            bookParticle(self.tree, label)
            var(self.tree, 'n_'+label)            
        for label in self.cfg_ana.jet_collections:  
            bookJet(self.tree, '{}_1'.format(label), self.taggers)
            bookJet(self.tree, '{}_2'.format(label), self.taggers)
        for label in self.cfg_ana.resonances:
            iso = False
            if 'zed' in label and not 'qq' in label:
                iso = True
            bookResonanceWithLegs(self.tree, label, iso)     
        bookResonanceWithLegs(self.tree, 'genboson1')
        bookResonanceWithLegs(self.tree, 'genboson2')
        for label in self.cfg_ana.misenergy:
            bookParticle(self.tree, label)        
        var(self.tree, 'n_nu')
        var(self.tree, 'beta4_chi2')
       
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
        for label in self.cfg_ana.particles:
            ptcs = getattr(event, label)
            fill(self.tree, 'n_'+label, len(ptcs))
            if len(ptcs):
                fillParticle(self.tree, label, ptcs[0])            
        for label in self.cfg_ana.jet_collections:  
            jets = getattr(event, label)
            for ijet, jet in enumerate(jets):
                if ijet == 2:
                    break
                fillJet(self.tree, '{label}_{ijet}'.format(label=label, ijet=ijet+1),
                        jet, self.taggers)
        for label in self.cfg_ana.resonances:
            resonances = getattr(event, label)
            if len(resonances)>0:  
                resonance = resonances[0]
                iso = False
                if 'zed' in label and not 'qq' in label:
                    iso = True                
                fillResonanceWithLegs(self.tree, label, resonance, iso)
        neutrinos = getattr(event, 'neutrinos', None)
        if neutrinos:
            fill(self.tree, 'n_nu', len(neutrinos))
        for i, boson in enumerate(event.gen_bosons[:2]):
            fillResonanceWithLegs(self.tree, 'genboson{i}'.format(i=i+1), boson)
        if hasattr(event, 'beta4_chi2'):
            fill(self.tree, 'beta4_chi2', event.beta4_chi2)
        self.tree.tree.Fill()
        
    def write(self, setup):
        self.rootfile.Write()
        self.rootfile.Close()
        
