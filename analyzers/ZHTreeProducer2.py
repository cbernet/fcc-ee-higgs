from heppy.framework.analyzer import Analyzer
from heppy.statistics.tree import Tree
from fcc_ee_higgs.analyzers.ntuple import *

from ROOT import TFile

def mkl(label, i=None):
    if i is None:
        return 'n_{}'.format(label)
    else:
        return '{}_{}'.format(label, i)
    
    
class ZHTreeProducer2(Analyzer):

    def _book(self, book_fun, cfg, *args, **kwargs):
        for label, n in cfg:
            var(self.tree, mkl(label))            
            for i in range(n):
                book_fun(self.tree, mkl(label, i), *args, **kwargs)    

    def _fill(self, fill_fun, cfg, event, *args, **kwargs):
        for label, n in cfg:
            ptcs = getattr(event, label)
            if not hasattr(ptcs, '__len__'):
                ptcs = [ptcs]
            fill(self.tree, mkl(label), len(ptcs))                
            for i, ptc in enumerate(ptcs):
                if i == n:
                    break
                fill_fun(self.tree, mkl(label, i), ptc, *args, **kwargs)
  

    def beginLoop(self, setup):
        super(ZHTreeProducer2, self).beginLoop(setup)
        self.rootfile = TFile('/'.join([self.dirName,
                                        'tree.root']),
                              'recreate')
        self.tree = Tree( 'events', '')
        
        self._book(bookParticle, self.cfg_ana.particles)
        self.taggers = ['b', 'bmatch', 'bfrac']   
        self._book(bookJet, self.cfg_ana.jets, self.taggers)
        self.iso = False
        self._book(bookResonanceWithLegs, self.cfg_ana.resonances, self.iso)
                
       
    def process(self, event):
        self.tree.reset()

        self._fill(fillParticle, self.cfg_ana.particles, event)
        self._fill(fillJet, self.cfg_ana.jets, event, self.taggers)
        self._fill(fillResonanceWithLegs, self.cfg_ana.resonances, event,
                   self.iso)
        self.tree.tree.Fill()
        
    def write(self, setup):
        self.rootfile.Write()
        self.rootfile.Close()
        
