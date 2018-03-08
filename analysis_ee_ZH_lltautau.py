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

zz = FCCComponent( 
    'pythia/ee_to_ZZ_Sep12_A_2',
    splitFactor=1
)

ww = FCCComponent( 
    'pythia/ee_to_WW_Dec6_large',
    splitFactor=1
)

ffbar = FCCComponent(
    'pythia/ee_to_ffbar_Sep12_B_4',
    splitFactor=1
)

ffbar2l = FCCComponent( 
    'pythia/ee_to_ffbar_2l_Mar6',
    splitFactor=1
)

import glob
test_files=glob.glob('Out_pythia_Zll_orsel/Job*/*.root')
test = cfg.Component(
    'zzll',
    files=test_files, 
    splitFactor=len(test_files)
)

cpslist = [
    ffbar2l, 
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


# gen Z

##from fcc_ee_higgs.analyzers.GenResonanceAnalyzer import GenResonanceAnalyzer
##gen_zeds_ll = cfg.Analyzer(
##    GenResonanceAnalyzer,
##    pdgids=[23],
##    statuses=[62],
##    decay_pdgids=[11, 13],
##    verbose=False
##)
##
##from heppy.analyzers.EventFilter   import EventFilter  
##gen_zeds_ll_counter = cfg.Analyzer(
##    EventFilter  ,
##    'gen_zeds_ll_counter',
##    input_objects = 'gen_bosons',
##    min_number = min_gen_z,
##    veto = False
##)

# gen bosons

from fcc_ee_higgs.analyzers.GenResonanceAnalyzer import GenResonanceAnalyzer
gen_bosons = cfg.Analyzer(
    GenResonanceAnalyzer,
    pdgids=[23, 25],
    statuses=[62],
    # decay_pdgids=[11, 13],
    verbose=False
)

# gen level filtering

gen_e_min = 5.

from heppy.analyzers.Selector import Selector
gen_eles = cfg.Analyzer(
    Selector,
    'gen_eles',
    output = 'gen_eles',
    input_objects = 'gen_particles',
    filter_func = lambda ptc: ptc.e() > gen_e_min and abs(ptc.pdgid()) == 11 and ptc.status() == 1
)

from heppy.analyzers.Selector import Selector
gen_mus = cfg.Analyzer(
    Selector,
    'gen_mus',
    output = 'gen_mus',
    input_objects = 'gen_particles',
    filter_func = lambda ptc: ptc.e() > gen_e_min and abs(ptc.pdgid()) == 13 and ptc.status() == 1
)

from fcc_ee_higgs.analyzers.GenDiLeptonFilter import GenDiLeptonFilter
gen_ll_filter = cfg.Analyzer(
    GenDiLeptonFilter,
    eles='gen_eles',
    mus='gen_mus'
)

gen_nus = cfg.Analyzer(
    Selector,
    'gen_nus',
    output = 'gen_nus',
    input_objects = 'gen_particles',
    filter_func = lambda ptc: abs(ptc.pdgid()) in [12, 14, 16] and ptc.status() == 1    
)

from heppy.analyzers.P4SumBuilder import P4SumBuilder
gen_missing_energy = cfg.Analyzer(
    P4SumBuilder,
    output = 'gen_missing_energy',
    particles = 'gen_nus', 
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

# Select isolated leptons with a Selector
# one can pass a function like this one to the filter:
def relative_isolation(lepton):
    sumpt = lepton.iso_211.sumpt + lepton.iso_22.sumpt + lepton.iso_130.sumpt
    sumpt /= lepton.pt()
    return sumpt
# ... or use a lambda statement as done below. 
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
zeds = cfg.Analyzer(
    ResonanceBuilder,
    output = 'zeds',
    leg_collection = 'sel_iso_leptons',
    pdgid = 23
)

zed_selector = cfg.Analyzer(
    Selector,
    'sel_zeds',
    output = 'sel_zeds',
    input_objects = 'zeds',
    nmax=1, 
    # filter_func=lambda zed: True,
    filter_func = lambda zed: zed.leg1().pdgid() == -zed.leg2().pdgid()
)

from heppy.analyzers.EventFilter   import EventFilter  
zed_counter = cfg.Analyzer(
    EventFilter  ,
    'zed_counter',
    input_objects = 'sel_zeds',
    min_number = min_rec_z,
    veto = False
)

from heppy.analyzers.ResonanceLegExtractor import ResonanceLegExtractor
leg_extractor = cfg.Analyzer(
    ResonanceLegExtractor,
    resonances = 'sel_zeds'
)

# Computing the recoil p4 (here, p_initial - p_zed)
# help(RecoilBuilder) for more information
sqrts = Collider.SQRTS 

from heppy.analyzers.RecoilBuilder import RecoilBuilder
recoil = cfg.Analyzer(
    RecoilBuilder,
    instance_label = 'recoil',
    output = 'recoil',
    sqrts = sqrts,
    to_remove = 'sel_zeds_legs'
) 

missing_energy = cfg.Analyzer(
    RecoilBuilder,
    instance_label = 'missing_energy',
    output = 'missing_energy',
    sqrts = sqrts,
    to_remove = 'rec_particles'
)

# Creating a list of particles excluding the decay products of the best zed.
# help(Masker) for more information
from heppy.analyzers.Masker import Masker
particles_not_zed = cfg.Analyzer(
    Masker,
    output = 'particles_not_zed',
    input = 'rec_particles',
    mask = 'sel_zeds_legs',
)

iso_leptons_not_zed = cfg.Analyzer(
    Masker,
    output = 'iso_leptons_not_zed',
    input = 'sel_iso_leptons',
    mask = 'sel_zeds_legs',
)

second_zeds = cfg.Analyzer(
    ResonanceBuilder,
    output = 'second_zeds',
    leg_collection = 'iso_leptons_not_zed',
    pdgid = 23
)

# Make jets from the particles not used to build the best zed.
# Here the event is forced into 2 jets to target ZH, H->b bbar)
# help(JetClusterizer) for more information
from heppy.analyzers.fcc.JetClusterizer import JetClusterizer
jets = cfg.Analyzer(
    JetClusterizer,
    output = 'jets',
    particles = 'particles_not_zed',
    fastjet_args = dict( njets = 2 ),
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

higgses = cfg.Analyzer(
    ResonanceBuilder,
    output = 'higgses',
    leg_collection = 'jets',
    pdgid = 25
)

# Analysis-specific ntuple producer
# please have a look at the code of the ZHTreeProducer class,
# in heppy/analyzers/examples/zh/ZHTreeProducer.py
from fcc_ee_higgs.analyzers.ZHTreeProducer import ZHTreeProducer
tree = cfg.Analyzer(
    ZHTreeProducer,
    jet_collections = ['jets'],
    resonances=['higgses', 'zeds', 'second_zeds'], 
    misenergy = ['missing_energy', 'gen_missing_energy'],
    recoil='recoil'
)

# definition of a sequence of analyzers,
# the analyzers will process each event in this order
sequence = cfg.Sequence(
    source,
    ##    gen_zeds_ll,
    ##    gen_zeds_ll_counter,
    gen_bosons, 
    gen_eles,
    gen_mus,
    gen_nus,
    gen_missing_energy, 
    gen_ll_filter, 
    papas_sequence,
    leptons,
    iso_leptons,
    sel_iso_leptons,
    zeds,
    zed_selector, 
    zed_counter,
    leg_extractor, 
    recoil,
    missing_energy,
    iso_leptons_not_zed,
    second_zeds, 
    particles_not_zed,
    jets,
    higgses, 
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
