from heppy.framework.analyzer import Analyzer

import sys
import itertools

from fcc_ee_higgs.analyzers.beta4 import beta4
from heppy.particles.tlv.resonance import Resonance2

class QQTauTauAnalyzer(Analyzer):

    def beginLoop(self, setup):
        super(QQTauTauAnalyzer, self).beginLoop(setup)
        self.counters.addCounter('cutflow')
        self.counters['cutflow'].register('All events')
        self.counters['cutflow'].register('2 taus')
        self.counters['cutflow'].register('3 taus')
        self.counters['cutflow'].register('4 taus')
    
    def process(self, event):
        jets = getattr(event, self.cfg_ana.jets)
        taus = getattr(event, self.cfg_ana.taus)
        self.counters['cutflow'].inc('All events')
        if len(taus) < 2:
            return False
        self.counters['cutflow'].inc('2 taus')
        if len(taus) == 3:
            self.counters['cutflow'].inc('3 taus')
        elif len(taus) == 4:
            self.counters['cutflow'].inc('4 taus')
        dmz = sys.float_info.max
        higgs = None
        zed = None
        besttaus = None
        bestjets = None
        first = True
        for tau1, tau2 in itertools.combinations(taus, 2):
            qqjetsp = [jet for jet in jets if jet not in [tau1, tau2]]
            assert(len(qqjetsp) == 2)
            zedp = Resonance2(qqjetsp[0], qqjetsp[1], 23, 1)
            dmzp = abs(zedp.m() - 91)
            if dmzp < dmz or first:
                first = False
                # the first flag ensures that the products are
                # calculated at least once.
                # rarely (~1 per mil), the rescaling goes completely
                # wrong and produce very high energy jets, hence
                # dmz much larger than the starting value
                dmz = dmzp
                higgs = Resonance2(tau1, tau2, 25, 1)
                zed = zedp
                besttaus = [tau1, tau2]
                bestjets = list(qqjetsp)
        setattr(event, 'bestjets', bestjets)
        setattr(event, 'besttaus', besttaus)        
        setattr(event, 'zedqqs', [zed])
        setattr(event, 'higgses', [higgs])        
        
