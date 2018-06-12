import heppy.framework.config as cfg

from heppy.analyzers.fcc.JetClusterizer import JetClusterizer
tau_jets = cfg.Analyzer(
    JetClusterizer,
    output = 'tau_jets',
    particles = 'rec_particles',
    fastjet_args = dict( R=0.2, p=-1, emin=5),
    verbose=False
)

from fcc_ee_higgs.analyzers.TauSelector import TauSelector
taus = cfg.Analyzer(
    TauSelector,
    output='taus', 
    jets='tau_jets',
    verbose=False
)

from heppy.analyzers.IsolationAnalyzer import IsolationAnalyzer
from heppy.particles.isolation import EtaPhiCircle
iso_taus = cfg.Analyzer(
    IsolationAnalyzer, 
    candidates = 'taus',
    particles = 'rec_particles',
    iso_area = EtaPhiCircle(0.4),
    off_iso_area =EtaPhiCircle(0.2)
    )

from heppy.analyzers.Selector import Selector
sel_iso_taus = cfg.Analyzer(
    Selector,
    'sel_iso_taus',
    output = 'sel_iso_taus',
    input_objects = 'taus',
    # filter_func = relative_isolation
    filter_func = lambda lep : lep.iso.sumpt/lep.pt()< 0.5
)

from heppy.analyzers.EventFilter   import EventFilter  
n_taus = cfg.Analyzer(
    EventFilter,
    'n_taus',
    input_objects = 'sel_iso_taus',
    min_number = 0,
    veto = False
)

isolated_taus_sequence = [
    tau_jets, 
    taus,
    iso_taus,
    sel_iso_taus,
    n_taus
]
