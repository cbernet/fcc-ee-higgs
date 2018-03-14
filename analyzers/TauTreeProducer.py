from heppy.framework.analyzer import Analyzer
from heppy.statistics.tree import Tree
from fcc_ee_higgs.analyzers.ntuple import *

from ROOT import TFile

class TauTreeProducer(Analyzer):

    def beginLoop(self, setup):
        super(TauTreeProducer, self).beginLoop(setup)
        self.rootfile = TFile('/'.join([self.dirName,
                                        'taus.root']),
                              'recreate')
        self.tree = Tree( 'events', '')
        bookJet(self.tree, 'tau')
        bookJet(self.tree, 'tau_match')        
       
    def process(self, event):
        self.tree.reset()
        taus = getattr(event, self.cfg_ana.taus)
        for tau in taus:
            fillJet(self.tree, 'tau', tau)
            if tau.match:
                fillJet(self.tree, 'tau_match', tau.match)
            self.tree.tree.Fill()
                
    def write(self, setup):
        self.rootfile.Write()
        self.rootfile.Close()
        
