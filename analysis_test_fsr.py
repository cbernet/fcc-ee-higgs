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
nfiles = 4 
# nfiles = 1
# mode = 'test'
min_gen_z = 0
min_rec_z = 1
from heppy.papas.detectors.CLIC import clic
from heppy.papas.detectors.CMS import cms
detector = clic

from fcc_datasets.fcc_component import FCCComponent

zh = FCCComponent( 
    'pythia/ee_to_ZH_Oct30',
    splitFactor=4
)

cpslist = [
    zh,
    # zz, ww, ffbar2l 
]

from fcc_ee_higgs.components.tools import get_components
selectedComponents = get_components(mode, cpslist, nfiles)
    
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

from heppy.test.papas_cfg import gen_particles_stable

from heppy.analyzers.Selector import Selector
leptons = cfg.Analyzer(
    Selector,
    'sel_leptons',
    output = 'leptons',
    input_objects = 'gen_particles_stable',
    filter_func = lambda ptc: ptc.e() > 5. and abs(ptc.pdgid()) in [11, 13] 
)

# Compute lepton isolation w/r other particles in the event.
# help(IsolationAnalyzer) for more information
from heppy.analyzers.IsolationAnalyzer import IsolationAnalyzer
from heppy.particles.isolation import EtaPhiCircle
iso_leptons = cfg.Analyzer(
    IsolationAnalyzer,
    candidates = 'leptons',
    particles = 'gen_particles_stable',
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
    min_number = 1, 
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

from fcc_ee_higgs.analyzers.ZHTreeProducer2 import ZHTreeProducer2
tree = cfg.Analyzer(
    ZHTreeProducer2,
    particles=[('recoil', 1)],
    iso_particles=[('sel_iso_leptons', 2)], 
    jets=[],
    resonances=[('sel_zeds', 1)], 
)

# definition of a sequence of analyzers,
# the analyzers will process each event in this order
sequence = cfg.Sequence(
    source,
    gen_particles_stable,
    leptons,
    iso_leptons,
    sel_iso_leptons, 
    zeds,
    zed_selector, 
    zed_counter,
    leg_extractor, 
    recoil,
    tree
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
