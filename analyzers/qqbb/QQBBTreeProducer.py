from heppy.framework.analyzer import Analyzer
from heppy.statistics.tree import Tree
from fcc_ee_higgs.analyzers.ntuple import *

from ROOT import TFile

class QQBBTreeProducer(Analyzer):

    def beginLoop(self, setup):
        super(QQBBTreeProducer, self).beginLoop(setup)
        self.rootfile = TFile('/'.join([self.dirName,
                                        'tree.root']),
                              'recreate')
        self.tree = Tree( 'events', '')
        self.taggers = ['b','bfrac', 'higgsmaker',
                        'n_constituents', 'n_charged_hadrons',
##                        'tageff', 'matched', 'dr', 'ancestor', 'parton', 'res',
##                        'higgs_from_pair', 'raw_e', 'raw_res'
                        ]

        bookJet(self.tree, 'hadjet1', self.taggers)
        bookJet(self.tree, 'hadjet2', self.taggers)
        bookJet(self.tree, 'hadjet3', self.taggers)
        bookJet(self.tree, 'hadjet4', self.taggers)

        bookParticle(self.tree, 'misenergy')
        bookIsoParticle(self.tree, 'lepton1')
        bookIsoParticle(self.tree, 'lepton2')
       
        bookResonanceWithLegs(self.tree, 'genboson1')
        bookResonanceWithLegs(self.tree, 'genboson2')
       
        var(self.tree, 'n_jets') 
        var(self.tree, 'n_leptons') 
        var(self.tree, 'n_candidates')
        var(self.tree, 'higgsmass') #Higgsmasse nach der Formel aus dem Paper
        var(self.tree, 'n_iso_leptons')

        var(self.tree, 'vismass')
        var(self.tree, 'chi2')
        var(self.tree, 'deltaWW')
        var(self.tree, 'deltaZZ')
        var(self.tree, 'm12')
        var(self.tree, 'm34')
        var(self.tree, 'mHJet')
        var(self.tree, 'mZedJet')
       
    def process(self, event):
        self.tree.reset()
        misenergy = getattr(event, self.cfg_ana.misenergy)
        fillParticle(self.tree, 'misenergy', misenergy )        

        hadjets = getattr(event, self.cfg_ana.hadjets)
        for ijet, jet in enumerate(hadjets):
            if ijet==4:
                break
            fillJet(self.tree, 'hadjet{ijet}'.format(ijet=ijet+1),
                    jet, self.taggers)

        try:
            fill(self.tree, 'higgsmass', getattr(event, self.cfg_ana.higgsmass))
        except AttributeError:
            pass

        leptons = getattr(event, self.cfg_ana.leptons)
        for ilep, lepton in enumerate(reversed(leptons)):
            if ilep == 2:
                break
            fillIsoParticle(self.tree,
                            'lepton{ilep}'.format(ilep=ilep+1), 
                            lepton)  
        
        for i, boson in enumerate(event.genbosons[:2]):
            fillResonanceWithLegs(self.tree, 'genboson{i}'.format(i=i+1), boson)

        fill( self.tree, 'n_jets', len(event.jets_inclusive) ) 
        fill( self.tree, 'n_leptons', len(leptons) )
        fill( self.tree, 'n_candidates', getattr(event, self.cfg_ana.numberOfCandidates))
        fill( self.tree, 'n_iso_leptons', len(event.sel_iso_leptons))

        fill(self.tree, 'vismass', event.sum_vis.m())
        
        fill(self.tree, 'chi2', getattr(event, self.cfg_ana.chi2))
        fill(self.tree, 'deltaWW', getattr(event, self.cfg_ana.dWW))
        fill(self.tree, 'deltaZZ', getattr(event, self.cfg_ana.dZZ))
        fill(self.tree, 'm12', getattr(event, self.cfg_ana.pair1_m))
        fill(self.tree, 'm34', getattr(event, self.cfg_ana.pair2_m))
        fill(self.tree, 'mHJet', getattr(event, self.cfg_ana.mHJet))
        fill(self.tree, 'mZedJet', getattr(event, self.cfg_ana.mZedJet)) 
        
        self.tree.tree.Fill()
    def write(self, setup):
        self.rootfile.Write()
        self.rootfile.Close()
        

