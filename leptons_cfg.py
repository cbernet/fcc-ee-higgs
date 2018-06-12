import heppy.framework.config as cfg

# Use a Selector to select leptons from the output of papas simulation.
# Currently, we're treating electrons and muons transparently.
# we could use two different instances for the Selector module
# to get separate collections of electrons and muons
# help(Selector) for more information
from heppy.analyzers.Selector import Selector
leptons = cfg.Analyzer(
    Selector,
    'sel_leptons',
    output = 'leptons',
    input_objects = 'rec_particles',
    filter_func = lambda ptc: ptc.e() > 5. and abs(ptc.pdgid()) in [11, 13]
)

# Compute lepton isolation w/r other particles in the event.
# help(IsolationAnalyzer) for more information
from heppy.analyzers.IsolationAnalyzer import IsolationAnalyzer
from heppy.particles.isolation import EtaPhiCircle
iso_leptons = cfg.Analyzer(
    IsolationAnalyzer,
    candidates = 'leptons',
    particles = 'rec_particles',
    iso_area = EtaPhiCircle(0.4)
)

sel_iso_leptons = cfg.Analyzer(
    Selector,
    'sel_iso_leptons',
    output = 'sel_iso_leptons',
    input_objects = 'leptons',
    # filter_func = relative_isolation
    filter_func = lambda lep : (lep.iso_211.sumpt + lep.iso_22.sumpt + lep.iso_130.sumpt) / lep.pt() < 0.5
)

from heppy.analyzers.EventFilter   import EventFilter  
n_leptons = cfg.Analyzer(
    EventFilter,
    'n_leptons',
    input_objects = 'sel_iso_leptons',
    min_number = 0,
    veto = False
)

isolated_leptons_sequence = [
    leptons,
    iso_leptons,
    sel_iso_leptons,
    n_leptons, 
]
