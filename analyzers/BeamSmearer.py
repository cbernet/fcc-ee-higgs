from heppy.framework.analyzer import Analyzer

import random
import pprint
import math
from ROOT import TLorentzVector

class BeamSmearer(Analyzer):
    
    def process(self, event):
        '''Smear the beam energy.
        
        The two incoming particle energies are smeared under
        a Gaussian pdf of width sigma relative to the beam energy
        
        All outgoing particles are then boosted to the new com
        system 
        '''
        genptcs = getattr(event, self.cfg_ana.gen_particles)
        sigma = self.cfg_ana.sigma
        f1 = random.gauss(1, sigma)
        f2 = random.gauss(1, sigma)
        
        beamptcs = [p for p in genptcs if p.status() == 4]
        pprint.pprint(beamptcs)
        
        assert(len(beamptcs) == 2)
        
        def smear(ptc, factor):
            e = ptc.p4().E() * factor
            pz = math.sqrt(e ** 2 - ptc.m() ** 2)
            if ptc.p4().Pz() < 0:
                pz = -pz                
            ptc._tlv.SetPxPyPzE( ptc.p4().Px(),
                                 ptc.p4().Py(),
                                 pz,
                                 e)        

        newcom = TLorentzVector()
        for ptc, factor in zip(beamptcs, [f1, f2]):
            smear(ptc, factor)
            ptc.p4().Print()
            print ptc.m()
            newcom += ptc.p4()
        
        print 'new com:'
        newcom.Print()
        boost = newcom.BoostVector()
        
        stablep4_before = TLorentzVector()
        stablep4 = TLorentzVector()
        for p in genptcs:
            if p in beamptcs:
                continue
            if p.status() == 1:
                stablep4_before += p._tlv
            # p._tlv.Boost(boost)
            p._tlv.Boost(boost)
            if p.status() == 1:
                stablep4 += p._tlv
                
        pprint.pprint(beamptcs)
        print newcom.E(), newcom.Pz()
        print stablep4.E(), stablep4.Pz()
        print stablep4_before.E(), stablep4_before.Pz()
        boost.Print()
        
        
