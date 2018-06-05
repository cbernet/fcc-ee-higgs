from heppy.framework.analyzer import Analyzer
from heppy.statistics.tree import Tree
from fcc_ee_higgs.analyzers.ntuple import *

from ROOT import TFile

class LLWWTreeProducer(Analyzer):

    def beginLoop(self, setup):
        super(LLWWTreeProducer, self).beginLoop(setup)
        self.rootfile = TFile('/'.join([self.dirName,
                                        'tree.root']),
                              'recreate')
        self.tree = Tree( 'events', '')
        if hasattr(self.cfg_ana, 'zeds'):  
            bookZed(self.tree, 'zed')

        for label in self.cfg_ana.misenergy:
            bookParticle(self.tree, label)
        
        # leptons
        self.nleptons_max = 2
        for label in self.cfg_ana.leptons:
            var(self.tree, 'n_'+label)
            for i in range(1, self.nleptons_max+1):            
                bookIsoParticle(self.tree, '{}_{}'.format(label, i))

        # jets
        self.taggers = ['b', 'bmatch', 'bfrac']
        self.njets_max = 4
        for label in self.cfg_ana.jet_collections:
            var(self.tree, 'n_'+label)
            for i in range(1, self.njets_max+1):
                bookJet(self.tree, '{}_{}'.format(label, i), self.taggers)
        bookJet(self.tree, 'sumjet_notzed')

        # global jet
        bookJet(self.tree, self.cfg_ana.globaljet)

        # resonances
        for label in self.cfg_ana.resonances:
            iso = False
            if 'zed' in label and not 'qq' in label:
                iso = True
            bookResonanceWithLegs(self.tree, label, iso)
        bookResonanceWithLegs(self.tree, 'genboson1')
        bookResonanceWithLegs(self.tree, 'genboson2')
        bookResonanceWithLegs(self.tree, 'genw1')
        bookResonanceWithLegs(self.tree, 'genw2')

##        if hasattr(self.cfg_ana, 'recoil'):
##            bookParticle(self.tree, 'recoil')

        for label in self.cfg_ana.particles:
            bookParticle(self.tree, label)
            var(self.tree, 'n_'+label)
            
        var(self.tree, 'n_nu')
##        var(self.tree, 'beta4_chi2')
       
    def process(self, event):
        self.tree.reset()

##        if len(event.sel_iso_leptons) == 2:
##            print event
##            print 
##
        if hasattr(self.cfg_ana, 'zeds'):  
            zeds = getattr(event, self.cfg_ana.zeds)
            if len(zeds)>0:
                zed = zeds[0].p
                fillZed(self.tree, 'zed', zed)
                
        for label in self.cfg_ana.misenergy:        
            misenergy = getattr(event, label)
            fillParticle(self.tree, label, misenergy)

        for label in self.cfg_ana.leptons:  
            leptons = getattr(event, label)
            fill(self.tree, 'n_{}'.format(label), len(leptons))
            for ilep, lep in enumerate(leptons):
                if ilep == self.nleptons_max:
                    break
                fillIsoParticle(self.tree,
                                '{label}_{ilep}'.format(label=label,
                                                        ilep=ilep+1),
                                lep)     
      
        # jets
        for label in self.cfg_ana.jet_collections:  
            jets = getattr(event, label)
            fill(self.tree, 'n_{}'.format(label), len(jets))
            for ijet, jet in enumerate(jets):
                if ijet == self.njets_max:
                    break
                fillJet(self.tree, '{label}_{ijet}'.format(label=label, ijet=ijet+1),
                        jet, self.taggers)
        
        # global jet  
        fillJet(self.tree, self.cfg_ana.globaljet, getattr(event, self.cfg_ana.globaljet))
        
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
        for i, boson in enumerate(event.gen_ws[:2]):
            fillResonanceWithLegs(self.tree, 'genw{i}'.format(i=i+1), boson)
            
##        if hasattr(self.cfg_ana, 'recoil'):
##            recoil = getattr(event, self.cfg_ana.recoil)    
##            fillParticle(self.tree, 'recoil', recoil)
        
        for label in self.cfg_ana.particles:
            ptcs = getattr(event, label)
            try:                
                fill(self.tree, 'n_'+label, len(ptcs))
                if len(ptcs):
                    fillParticle(self.tree, label, ptcs[0])
            except TypeError:
                # ptcs is a particle, not a list of ptcs
                fill(self.tree, 'n_'+label, 1)
                fillParticle(self.tree, label, ptcs)
                
                    
        self.tree.tree.Fill()
        
    def write(self, setup):
        self.rootfile.Write()
        self.rootfile.Close()
        
