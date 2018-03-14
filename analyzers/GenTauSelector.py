from heppy.framework.analyzer import Analyzer
from heppy.particles.genbrowser import GenBrowser
from heppy.particles.jet import group_pdgid, JetConstituents
from heppy.particles.tlv.jet import Jet as GenTau
from ROOT import TLorentzVector

import math

import pprint

class GenTauSelector(Analyzer):

    def process(self, event):
        gens = getattr(event, self.cfg_ana.gen_particles)
        gen_taus = [gen for gen in gens if abs(gen.pdgid()) == 15
                   and gen.status() == 2]
##        pprint.pprint(gen_taus)
        
        if not hasattr(event, 'genbrowser'):
            event.genbrowser = GenBrowser(event.gen_particles,
                                          event.gen_vertices)
        thetamax = 75. * math.pi / 180.
        acceptance = {
            211: lambda ptc: ptc.pt() > 0.3 and abs(ptc.theta()) < thetamax, 
            11: lambda ptc: ptc.e() > 5 and abs(ptc.theta()) < thetamax,
            13: lambda ptc: ptc.e() > 7.5 and abs(ptc.theta()) < thetamax,
        }
        acc_taus = []
        gen_taus_decayed = []
        for tau in gen_taus:
##            print tau
            ncharged = 0
            acc_charged = []
            descendants = event.genbrowser.descendants(tau)
            stable_daugthers = [desc for desc in descendants
                                if desc.status() == 1]
            consts = JetConstituents()
            p4sum = TLorentzVector()
            for dau in stable_daugthers:
                assert(dau.status() == 1)
##                print '\t', dau
                if abs(dau.pdgid()) in [12, 14, 16]:
                    continue
                p4sum += dau.p4()
                consts.append(dau)
                pdgid = group_pdgid(dau)
                if dau.q() and acceptance[pdgid](dau):
                    acc_charged.append(dau)
            gen_tau_decayed = GenTau( p4sum )
            gen_tau_decayed.constituents = consts
            gen_taus_decayed.append(gen_tau_decayed)

            if len(acc_charged) in [1, 3]:
                acc_taus.append(gen_tau_decayed)

        event.gen_taus = gen_taus_decayed
        event.gen_taus_acc = acc_taus
