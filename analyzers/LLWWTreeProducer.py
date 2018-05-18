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

        # resonances
        for label in self.cfg_ana.resonances:
            iso = False
            if 'zed' in label and not 'qq' in label:
                iso = True
            bookResonanceWithLegs(self.tree, label, iso)
        bookResonanceWithLegs(self.tree, 'genboson1')
        bookResonanceWithLegs(self.tree, 'genboson2')

        var(self.tree, 'n_nu')
##        var(self.tree, 'beta4_chi2')
       
    def process(self, event):
        self.tree.reset()

        if hasattr(self.cfg_ana, 'zeds'):  
            zeds = getattr(event, self.cfg_ana.zeds)
            if len(zeds)>0:
                zed = zeds[0]
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
      
        for label in self.cfg_ana.jet_collections:  
            jets = getattr(event, label)
            fill(self.tree, 'n_{}'.format(label), len(jets))
            for ijet, jet in enumerate(jets):
                if ijet == self.njets_max:
                    break
                fillJet(self.tree, '{label}_{ijet}'.format(label=label, ijet=ijet+1),
                        jet, self.taggers)
                
        fillJet(self.tree, 'sumjet_notzed', event.sum_particles_not_zed)
                             
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
##        if hasattr(event, 'beta4_chi2'):
##            fill(self.tree, 'beta4_chi2', event.beta4_chi2)
        self.tree.tree.Fill()
        
    def write(self, setup):
        self.rootfile.Write()
        self.rootfile.Close()
        
