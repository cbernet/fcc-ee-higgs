'''Example configuration file for an ee->ZH->mumubb analysis in heppy, with the FCC-ee

While studying this file, open it in ipython as well as in your editor to 
get more information: 

ipython
from analysis_ee_ZH_cfg import * 
'''
import sys
import os
import copy
import heppy.framework.config as cfg

import logging

# next 2 lines necessary to deal with reimports from ipython
logging.shutdown()
reload(logging)


# global logging level for the heppy framework.
# in addition, all the analyzers declared below have their own logger,
# an each of them can be set to a different logging level.
logging.basicConfig(level=logging.WARNING)

# setting the random seed for reproducible results
import heppy.statistics.rrandom as random
# do not forget to comment out the following line if you want to produce and combine
# several samples of events 
random.seed(0xdeadbeef)

# loading the FCC event data model library to decode
# the format of the events in the input file
# help(Events) for more information 
from ROOT import gSystem
gSystem.Load("libdatamodelDict")
from EventStore import EventStore as Events

# setting the event printout
# help(Event) for more information
from heppy.framework.event import Event
# comment the following line to see all the collections stored in the event 
# if collection is listed then print loop.event.papasevent will include the collections
Event.print_patterns=['gen_bosons', '*zeds*', 'higgs*', 'jets*', 'bquarks', 'recoil*', 'collections']

# definition of the collider
# help(Collider) for more information
from heppy.configuration import Collider
Collider.BEAMS = 'ee'
Collider.SQRTS = 240.

jet_correction = True

# import pdb; pdb.set_trace()
# mode = 'pythia/ee_to_ZH_Oct30'
# mode = 'pythia/ee_to_ZZ_Sep12_A_2'
mode = 'all'
nfiles = sys.maxint
# nfiles = 1
# mode = 'test'
min_gen_z = 0
min_rec_z = 1
from heppy.papas.detectors.CLIC import clic
from heppy.papas.detectors.CMS import cms
detector = clic

### definition of input samples                                                                                                   
### from components.ZH_Znunu import components as cps
##from fcc_ee_higgs.components.all import load_components
##cps = load_components(mode='pythia')

from fcc_datasets.fcc_component import FCCComponent

zh = FCCComponent( 
    'pythia/ee_to_ZH_Oct30',
    splitFactor=4
)
##
##zz = FCCComponent( 
##    'pythia/ee_to_ZZ_Sep12_A_2',
##    splitFactor=1
##)
##
##ww = FCCComponent( 
##    'pythia/ee_to_WW_Dec6_large',
##    splitFactor=1
##)
##
##ffbar = FCCComponent(
##    'pythia/ee_to_ffbar_Sep12_B_4',
##    splitFactor=1
##)
##
##ffbar2l = FCCComponent( 
##    'pythia/ee_to_ffbar_2l_Mar6',
##    splitFactor=1
##)

import glob
test_files=glob.glob('ee_ZH_Htautau.root')
test = cfg.Component(
    'zzll',
    files=test_files, 
    splitFactor=len(test_files)
)

cpslist = [
    test, 
]

cps = dict( (c.name, c) for c in cpslist)

selectedComponents = cps.values()                                                                                      
for comp in selectedComponents:
    comp.splitFactor = min(len(comp.files),nfiles)

test_filename = os.path.abspath('samples/test/ee_ZH_Hbb.root')
if mode == 'test':
    comp = cps['pythia/ee_to_ZH_Oct30']
    comp.files = [test_filename]
    comp.splitFactor = 1
    selectedComponents = [comp]
elif mode == 'all':
    selectedComponents = cps.values()                      
else:
    selectedComponents = [cps[mode]]

if nfiles: 
    for cp in cps.values():
        cp.files = cp.files[:nfiles]
 
##zh.files = 'ee_ZH_Zmumu_Htautau.root'
##zh.splitFactor = 1 
    
# read FCC EDM events from the input root file(s)
# do help(Reader) for more information
from heppy.analyzers.fcc.Reader import Reader
source = cfg.Analyzer(
    Reader,
    gen_particles = 'GenParticle',
    gen_vertices = 'GenVertex'
)

# gen bosons

from fcc_ee_higgs.analyzers.GenResonanceAnalyzer import GenResonanceAnalyzer
gen_bosons = cfg.Analyzer(
    GenResonanceAnalyzer,
    pdgids=[23, 25],
    statuses=[62],
    # decay_pdgids=[11, 13],
    verbose=False
)

# importing the papas simulation and reconstruction sequence,
# as well as the detector used in papas
# check papas_cfg.py for more information
from heppy.test.papas_cfg import papas, pfreconstruct, papas_sequence
from heppy.test.papas_cfg import papasdisplaycompare as display 

papas.detector = detector    
display.detector = detector
pfreconstruct.detector = detector

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
    filter_func = lambda lep : lep.iso.sumpt/lep.pt()< 0.5
)

# Building Zeds
# help(ResonanceBuilder) for more information
from heppy.analyzers.ResonanceBuilder import ResonanceBuilder
zedlls = cfg.Analyzer(
    ResonanceBuilder,
    output = 'zedlls',
    leg_collection = 'sel_iso_leptons',
    pdgid = 23
)

from heppy.analyzers.ResonanceLegExtractor import ResonanceLegExtractor
leg_extractor = cfg.Analyzer(
    ResonanceLegExtractor,
    resonances = 'zedlls'
)

# Computing the recoil p4 (here, p_initial - p_zed)
# help(RecoilBuilder) for more information
sqrts = Collider.SQRTS 

from heppy.analyzers.RecoilBuilder import RecoilBuilder
missing_energy = cfg.Analyzer(
    RecoilBuilder,
    instance_label = 'missing_energy',
    output = 'missing_energy',
    sqrts = sqrts,
    to_remove = 'rec_particles'
)

# Make jets from the particles not used to build the best zed.
# Here the event is forced into 2 jets to target ZH, H->b bbar)
# help(JetClusterizer) for more information
from heppy.analyzers.fcc.JetClusterizer import JetClusterizer
jets = cfg.Analyzer(
    JetClusterizer,
    output = 'jets',
    particles = 'rec_particles',
    fastjet_args = dict( njets = 4),
    njets_required=False
)

if jet_correction:
    from heppy.analyzers.JetEnergyCorrector import JetEnergyCorrector
    jets_cor = cfg.Analyzer(
        JetEnergyCorrector,
        input_jets='jets',
        detector=detector 
    )
    jets = cfg.Sequence(jets, jets_cor)

from fcc_ee_higgs.analyzers.Beta4Rescaler import Beta4Rescaler
beta4rescaler = cfg.Analyzer(
    Beta4Rescaler,
    output='jets_rescaled', 
    jets='jets'
)

from fcc_ee_higgs.analyzers.TauSelector import TauSelector
from heppy.analyzers.Masker import Masker

taus = cfg.Analyzer(
    TauSelector,
    output='taus', 
    jets='jets'
)

higgses = cfg.Analyzer(
    ResonanceBuilder,
    output = 'higgses',
    leg_collection = 'taus',
    pdgid = 25
)

jets_not_taus = cfg.Analyzer(
    Masker,
    output = 'jets_not_taus',
    input = 'jets',
    mask = 'taus',
)

zedqqs = cfg.Analyzer(
    ResonanceBuilder,
    output = 'zedqqs',
    leg_collection = 'jets_not_taus',
    pdgid = 23
)

taus_rescaled = cfg.Analyzer(
    TauSelector,
    output='taus_rescaled', 
    jets='jets_rescaled'
)

higgses_rescaled = cfg.Analyzer(
    ResonanceBuilder,
    output = 'higgses_rescaled',
    leg_collection = 'taus_rescaled',
    pdgid = 25
)

jets_not_taus_rescaled = cfg.Analyzer(
    Masker,
    output = 'jets_not_taus_rescaled',
    input = 'jets_rescaled',
    mask = 'taus_rescaled',
)

zedqqs_rescaled = cfg.Analyzer(
    ResonanceBuilder,
    output = 'zedqqs_rescaled',
    leg_collection = 'jets_not_taus_rescaled',
    pdgid = 23
)

# Analysis-specific ntuple producer
# please have a look at the code of the ZHTreeProducer class,
# in heppy/analyzers/examples/zh/ZHTreeProducer.py
from fcc_ee_higgs.analyzers.ZHTreeProducer import ZHTreeProducer
tree = cfg.Analyzer(
    ZHTreeProducer,
    jet_collections = ['jets', 'jets_rescaled', 'taus', 'taus_rescaled'],
    resonances=['higgses', 'higgses_rescaled', 'zedlls', 'zedqqs', 'zedqqs_rescaled'], 
    misenergy = ['missing_energy'],
    particles=[], 
)

# definition of a sequence of analyzers,
# the analyzers will process each event in this order
sequence = cfg.Sequence(
    source,
    gen_bosons, 
    papas_sequence,
    leptons,
    iso_leptons,
    sel_iso_leptons,
    zedlls,
    leg_extractor, 
    missing_energy,
    jets,
    beta4rescaler, 
    taus, 
    higgses,
    jets_not_taus,
    zedqqs,
    taus_rescaled,
    higgses_rescaled,
    jets_not_taus_rescaled,
    zedqqs_rescaled, 
    tree,
    display
)   

# Specifics to read FCC events 
from ROOT import gSystem
gSystem.Load("libdatamodelDict")
from EventStore import EventStore as Events

config = cfg.Config(
    components = selectedComponents,
    sequence = sequence,
    services = [],
    events_class = Events
)
