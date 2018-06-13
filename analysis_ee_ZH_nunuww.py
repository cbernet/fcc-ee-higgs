'''Example configuration file for an ee->ZH->mumubb analysis in heppy, with the FCC-ee

While studying this file, open it in ipython as well as in your editor to 
get more information: 

ipython
from analysis_ee_ZH_cfg import * 
'''

import os
import sys
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
Event.print_patterns=['zeds*', 'higgs*', 'jets*', 'bquarks', 'recoil*', 'collections']

# definition of the collider
# help(Collider) for more information
from heppy.configuration import Collider
Collider.BEAMS = 'ee'
Collider.SQRTS = 240.

jet_correction = True

# mode = 'pythia/ee_to_ffbar_Sep12_B_4'
mode =  'all'
nfiles = None


from heppy.papas.detectors.CLIC import clic
from heppy.papas.detectors.CMS import cms
detector = clic

### definition of input samples                                                                                                   
### from components.ZH_Znunu import components as cps
##from fcc_ee_higgs.components.all import load_components
##cps = load_components(mode='pythia')

from fcc_datasets.fcc_component import FCCComponent
zz = FCCComponent( 
    'pythia/ee_to_ZZ_Sep12_A_2',
    splitFactor=1
)

zh = FCCComponent( 
    'pythia/ee_to_ZH_Oct30',
    splitFactor=1
)

ffbar = FCCComponent( 
    'pythia/ee_to_ffbar_Sep12_B_4',
    splitFactor=1
)

ww = FCCComponent( 
    'pythia/ee_to_WW_Dec6_large',
    splitFactor=1
)

#zh_nunuwwqq = FCCComponent( 
#    'pythia/ee_ZH_Znunu_HWW_Wqq',
#    splitFactor=1
#)   

from fcc_ee_higgs.components.tools import get_components
selectedComponents = get_components(mode, [zz,zh,ffbar,ww], nfiles)


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

gen_ws = cfg.Analyzer(
    GenResonanceAnalyzer,
    output='gen_ws', 
    pdgids=[24],
    statuses=[22],
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

sqrts = Collider.SQRTS 

# leptons, for veto
from fcc_ee_higgs.leptons_cfg import isolated_leptons_sequence, n_leptons
n_leptons.min_number = 1
n_leptons.veto = True

# taus, for veto
from fcc_ee_higgs.taus_cfg import isolated_taus_sequence, sel_iso_taus, n_taus
sel_iso_taus.filter_func = lambda lep : lep.iso.sumpt/lep.pt()< 0.5
n_taus.min_number = 0
n_taus.veto = False

from heppy.analyzers.fcc.JetClusterizer import JetClusterizer
jets_inclusive = cfg.Analyzer(
    JetClusterizer,
    output = 'jets_inclusive',
    particles = 'rec_particles',
    #particles = 'gen_particles_stable',
    fastjet_args = dict(R=0.4, p=-1, emin=5),  ##Colin replaced by lower E cut
)

# veto events with a jet with < 3 charged hadrons
from heppy.analyzers.Selector import Selector
jets_inclusive_small = cfg.Analyzer(
    Selector,
    'jets_inclusive_small',
    output = 'jets_inclusive_small',
    input_objects = 'jets_inclusive',
    filter_func = lambda j: j.constituents[211].num < 3
)

from heppy.analyzers.EventFilter   import EventFilter  
n_jets_small = cfg.Analyzer(
    EventFilter,
    'n_jets_small',
    input_objects = 'jets_inclusive_small',
    min_number = 1,
    veto =True
)

n_jets_inclusive = cfg.Analyzer(
    EventFilter,
    'n_jets_inclusive',
    input_objects = 'jets_inclusive',
    min_number = 4,
    veto =False
)


# Make jets from the particles not used to build the best zed.
# Here the event is forced into 2 jets to target ZH, H->b bbar)
# help(JetClusterizer) for more information
from heppy.analyzers.fcc.JetClusterizer import JetClusterizer
jets4 = cfg.Analyzer(
    JetClusterizer,
    output = 'jets4',
    particles = 'rec_particles',
    fastjet_args = dict( njets = 4 ),
    njets_required=False
)

from fcc_ee_higgs.analyzers.NuNuWWAnalyzer import NuNuWWAnalyzer
nunuww = cfg.Analyzer(
    NuNuWWAnalyzer,
    jets='jets4'
)

jets2 = cfg.Analyzer(
    JetClusterizer,
    output = 'jets2',
    particles = 'rec_particles',
    fastjet_args = dict( njets = 2 ),
    njets_required=False
)


from fcc_ee_higgs.analyzers.ZHnunubbJetRescaler import ZHnunubbJetRescaler
jet_rescaling = cfg.Analyzer(
    ZHnunubbJetRescaler,
    output='jets2_rescaled', 
    jets='jets2',
    verbose=False
)

from heppy.analyzers.RecoilBuilder import RecoilBuilder
missing_energy = cfg.Analyzer(
    RecoilBuilder,
    instance_label = 'missing_energy',
    output = 'missing_energy',
    sqrts = sqrts,
    to_remove = 'jets2'
) 

missing_energy_rescaled = cfg.Analyzer(
    RecoilBuilder,
    instance_label = 'missing_energy_rescaled',
    output = 'missing_energy_rescaled',
    sqrts = sqrts,
    to_remove = 'jets2_rescaled'
) 

# b tagging 
from heppy.test.btag_parametrized_cfg import btag_parametrized, btag
btag.input_jets = 'jets4'

# Build Higgs candidates from pairs of jets.
from heppy.analyzers.ResonanceBuilder import ResonanceBuilder

higgses = cfg.Analyzer(
    ResonanceBuilder,
    output = 'higgses',
    leg_collection = 'jets2',
    pdgid = 25
)

higgses_rescaled = cfg.Analyzer(
    ResonanceBuilder,
    output = 'higgses_rescaled',
    leg_collection = 'jets2_rescaled',
    pdgid = 25
)

# Analysis-specific ntuple producer
# please have a look at the code of the ZHTreeProducer class,
# in heppy/analyzers/examples/zh/ZHTreeProducer.py
from fcc_ee_higgs.analyzers.ZHTreeProducer2 import ZHTreeProducer2
tree = cfg.Analyzer(
    ZHTreeProducer2,
    particles=[('missing_energy', 1),
               ('missing_energy_rescaled', 1)],
    iso_particles=[('sel_iso_taus', 4), ('sel_iso_leptons', 1)], 
    jets=[('jets4', 4), 
          ('jets2', 2), 
          ('jets2_rescaled', 2)],
    resonances=[('higgses', 1),
                ('higgses_rescaled', 1),
                ('w', 1),
                ('wstar', 1)], 
)

# definition of a sequence of analyzers,
# the analyzers will process each event in this order
sequence = cfg.Sequence(
    source,
    gen_bosons,
    gen_ws, 
    papas_sequence,
    isolated_leptons_sequence,
    isolated_taus_sequence,
    jets_inclusive,
    n_jets_inclusive, 
    jets_inclusive_small,
    n_jets_small, 
    jets4,
    nunuww, 
    jets2, 
    jet_rescaling, 
    btag_parametrized,
    missing_energy,
    missing_energy_rescaled, 
    higgses,
    higgses_rescaled, 
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
