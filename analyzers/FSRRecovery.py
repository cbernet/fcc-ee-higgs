from heppy.framework.analyzer import Analyzer
from heppy.utils.deltar import deltaR2

import pprint
import copy

from ROOT import TLorentzVector

class FSRRecovery(Analyzer):
    
    def process(self, event):
        zed = getattr(event, self.cfg_ana.zeds)[0]
        particles = getattr(event, self.cfg_ana.particles)
        photons = [ptc for ptc in particles if ptc.pdgid() == 22]
        area = self.cfg_ana.area
        # sort photons according to distance to one of the leptons
        sorted_photons = []
        for photon in photons:
            if not area.is_inside(zed.leg1(), photon) and \
               not area.is_inside(zed.leg2(), photon):
                continue
            dr2_1 = deltaR2(photon, zed.leg1())
            dr2_2 = deltaR2(photon, zed.leg2())
            mindr2 = dr2_2
            leg = 1
            if dr2_1 < dr2_2:
                mindr2 = dr2_1
                leg = 0
            sorted_photons.append( (mindr2, leg, photon) )
            # print mindr2
            # print photon
            # pprint.pprint(zed.legs)
            # print
        sorted_photons.sort()
##        pprint.pprint(zed.legs)
##        pprint.pprint(sorted_photons)
##        print
        # loop on sorted photons and append to Z while Z mass
        # improved
        mz = 91.1876
        oldmass = zed.m()
        newzed = None
        for dummy, leg, photon in sorted_photons:
            # print photon
            newp4 = TLorentzVector(zed.p4())
            newp4 += photon.p4()
            newmass = newp4.M()
            # print oldmass, newmass
            if abs(newmass - mz) < abs(oldmass-mz):
                # print 'adding photon'
                if newzed is None:
                    if hasattr(self.cfg_ana, 'output'):
                        newzed = copy.deepcopy(zed)
                    else:
                        newzed = zed
                newzed._tlv = newp4
                newzed.legs[leg]._tlv += photon.p4()
                oldmass = newmass
                # need to change leg iso
        if hasattr(self.cfg_ana, 'output'):
            if newzed is None:
                newzed = zed
            setattr(event, self.cfg_ana.output, [newzed])

        
