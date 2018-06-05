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
Event.print_patterns=['gen_bosons', 'gen_ws', 'gen_particles*',
                      'rec_particles', 'sel_iso_leptons','*zeds*', 'jets*',
                      'sum_particles_not_leptons', 'collections']

# definition of the collider
# help(Collider) for more information
from heppy.configuration import Collider
Collider.BEAMS = 'ee'
Collider.SQRTS = 240.

jet_correction = True

##mode = 'pythia/ee_to_ZH_Zqq_HWW'
##nfiles = 1

mode = 'all'
nfiles = None

from heppy.papas.detectors.CLIC import clic
from heppy.papas.detectors.CMS import cms
detector = clic

### definition of input samples                                                                                                   

from fcc_datasets.fcc_component import FCCComponent

zh = FCCComponent( 
    'pythia/ee_to_ZH_Oct30',
    splitFactor=4
)

zh_qqww = FCCComponent( 
    'pythia/ee_to_ZH_Zqq_HWW_Wll',
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

ffbar2l = FCCComponent( 
    'pythia/ee_to_2l_Mar8',
    splitFactor=1
)

from fcc_ee_higgs.components.tools import get_components
selectedComponents = get_components(mode, [zh_qqww], nfiles)

# read FCC EDM events from the input root file(s)
# do help(Reader) for more information
from heppy.analyzers.fcc.Reader import Reader
source = cfg.Analyzer(
    Reader,
    gen_particles = 'GenParticle',
    gen_vertices = 'GenVertex'
)

from heppy.analyzers.EventByNumber import EventByNumber
event_by_number = cfg.Analyzer(
    EventByNumber,
    event_numbers=[30]
)

from heppy.analyzers.EventSkipper import EventSkipper
event_skipper = cfg.Analyzer(
    EventSkipper,
    first_event=58
)

# gen bosons

from fcc_ee_higgs.analyzers.GenResonanceAnalyzer import GenResonanceAnalyzer
gen_bosons = cfg.Analyzer(
    GenResonanceAnalyzer,
    output='gen_bosons', 
    pdgids=[23, 25],
    statuses=[62],
    # decay_pdgids=[11, 13],
    verbose=False
)

gen_ws = cfg.Analyzer(
    GenResonanceAnalyzer,
    output='gen_ws', 
    pdgids=[24],
    statuses=[22],
    verbose=False    
)

# gen level filtering: 2 leptons

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
    mus='gen_mus',
    same_flavour=False
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

sel_iso_leptons = cfg.Analyzer(
    Selector,
    'sel_iso_leptons',
    output = 'sel_iso_leptons',
    input_objects = 'leptons',
    # filter_func = relative_isolation
    filter_func = lambda lep : (lep.iso_211.sumpt + lep.iso_22.sumpt + lep.iso_130.sumpt) / lep.pt() < 0.5
)

# Building Zeds
# help(ResonanceBuilder) for more information
from heppy.analyzers.ResonanceBuilder import ResonanceBuilder
zeds_lep = cfg.Analyzer(
    ResonanceBuilder,
    output = 'zeds_lep',
    leg_collection = 'sel_iso_leptons',
    pdgid = 23
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

# Creating a list of particles excluding the decay products of the best zed.
# help(Masker) for more information
from heppy.analyzers.Masker import Masker
particles_not_leptons = cfg.Analyzer(
    Masker,
    output = 'particles_not_leptons',
    input = 'rec_particles',
    mask = 'sel_iso_leptons',
)

# Make jets 
from heppy.analyzers.fcc.JetClusterizer import JetClusterizer
jets = cfg.Analyzer(
    JetClusterizer,
    output = 'jets',
    particles = 'particles_not_leptons',
    fastjet_args = dict( njets = 2),
    verbose=False
)

if jet_correction:
    from heppy.analyzers.JetEnergyCorrector import JetEnergyCorrector
    jets_cor = cfg.Analyzer(
        JetEnergyCorrector,
        input_jets='jets',
        detector=detector 
    )
    jets = cfg.Sequence(jets, jets_cor)

from heppy.analyzers.RecoilBuilder import RecoilBuilder
recoil_had = cfg.Analyzer(
    RecoilBuilder,
    instance_label = 'recoil_had',
    output = 'recoil_had',
    sqrts = sqrts,
    to_remove = 'jets'
)

from heppy.analyzers.ResonanceBuilder import ResonanceBuilder
zeds = cfg.Analyzer(
    ResonanceBuilder,
    output = 'zeds',
    leg_collection = 'jets',
    pdgid = 23    
)
    
from heppy.analyzers.SingleJetBuilder import SingleJetBuilder
sum_particles_not_leptons = cfg.Analyzer(
    SingleJetBuilder, 
    output='sum_particles_not_leptons',
    particles='particles_not_leptons'
)

# b tagging

from heppy.test.btag_parametrized_cfg import btag_parametrized, btag
btag.roc = None

# Analysis-specific ntuple producer
# please have a look at the code of the ZHTreeProducer class,
# in heppy/analyzers/examples/zh/ZHTreeProducer.py
from fcc_ee_higgs.analyzers.LLWWTreeProducer import LLWWTreeProducer
tree = cfg.Analyzer(
    LLWWTreeProducer,
    jet_collections = ['jets'],
    resonances=['zeds_lep'], 
    misenergy = ['missing_energy', 'gen_missing_energy'],
    leptons=['sel_iso_leptons'],
    particles=['particles_not_leptons',
               'recoil_had',
               'zeds'],
    globaljet='sum_particles_not_leptons', 
)

# definition of a sequence of analyzers,
# the analyzers will process each event in this order
sequence = cfg.Sequence(
    source,
    # event_by_number,
    # event_skipper, 
    ##    gen_zeds_ll,
    ##    gen_zeds_ll_counter,
    # gen_taus,
    # two_gen_taus_in_acceptance, 
    gen_bosons,
    gen_ws, 
    gen_eles,
    gen_mus,
    gen_nus,
    gen_missing_energy, 
    gen_ll_filter, 
    papas_sequence,
    leptons,
    iso_leptons,
    sel_iso_leptons,
    zeds_lep,
##    recoil_lep,
    missing_energy,
    particles_not_leptons,
    jets,
    recoil_had,
    zeds, 
    btag_parametrized,
    sum_particles_not_leptons, 
    tree,
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
