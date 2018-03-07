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

# mode = 'pythia/ee_to_ZZ_Sep12_A_2'
nfiles = sys.maxint
# mode = 'debug'
mode = 'all'
from heppy.papas.detectors.CLIC import clic
from heppy.papas.detectors.CMS import cms
detector = cms

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



cpslist = [
    # zz,
    # zh,
    # ffbar,
    ww, 
]

cps = dict( (c.name, c) for c in cpslist)

selectedComponents = cps.values()                                                                                      
for comp in selectedComponents:
    comp.splitFactor = min(len(comp.files),nfiles)

test_filename = os.path.abspath('samples/test/ee_ZZ_nunu.root')
if mode == 'test':
    comp = cps['pythia/ee_to_ZZ_Sep12_A_2']
    comp.files = [test_filename]
    comp.splitFactor = 1
    selectedComponents = [comp]
elif mode == 'debug':
    comp = cpslist[0]
    comp.files = comp.files[:1]
    comp.splitFactor = 1 
    selectedComponents = [comp]
elif mode == 'all':
    selectedComponents = cps.values()                      
else:
    selectedComponents = [cps[mode]]

if nfiles: 
    for cp in cps.values():
        cp.files = cp.files[:nfiles]
    
# read FCC EDM events from the input root file(s)
# do help(Reader) for more information
from heppy.analyzers.fcc.Reader import Reader
source = cfg.Analyzer(
    Reader,
    gen_particles = 'GenParticle',
    gen_vertices = 'GenVertex'
)

from fcc_ee_higgs.analyzers.GenResonanceAnalyzer import GenResonanceAnalyzer
gen_ana = cfg.Analyzer(
    GenResonanceAnalyzer,
    pdgids=[23, 25],
    statuses=[62]
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

from heppy.analyzers.RecoilBuilder import RecoilBuilder
missing_energy = cfg.Analyzer(
    RecoilBuilder,
    instance_label = 'missing_energy',
    output = 'missing_energy',
    sqrts = sqrts,
    to_remove = 'jets'
) 

missing_energy_rescaled = cfg.Analyzer(
    RecoilBuilder,
    instance_label = 'missing_energy_rescaled',
    output = 'missing_energy_rescaled',
    sqrts = sqrts,
    to_remove = 'jets_rescaled'
) 

# Make jets from the particles not used to build the best zed.
# Here the event is forced into 2 jets to target ZH, H->b bbar)
# help(JetClusterizer) for more information
from heppy.analyzers.fcc.JetClusterizer import JetClusterizer
jets = cfg.Analyzer(
    JetClusterizer,
    output = 'jets',
    particles = 'rec_particles',
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

from fcc_ee_higgs.analyzers.ZHnunubbJetRescaler import ZHnunubbJetRescaler
jet_rescaling = cfg.Analyzer(
    ZHnunubbJetRescaler,
    output='jets_rescaled', 
    jets='jets',
    verbose=False
)

# b tagging 
from heppy.test.btag_parametrized_cfg import btag_parametrized, btag

##from heppy.analyzers.roc import cms_roc
##btag.roc = None
##
##def is_bjet(jet):
##    return jet.tags['b'] == 1
##bjets = cfg.Analyzer(
##    Selector,
##    'bjets',
##    output = 'bjets',
##    input_objects = 'jets',
##    filter_func = lambda jet: jet.tags['b'] == 1
##)
##
##onebjet = cfg.Analyzer(
##    EventFilter  ,
##    'onebjet',
##    input_objects = 'bjets',
##    min_number = 1,
##    veto = False
##)

# Build Higgs candidates from pairs of jets.
from heppy.analyzers.ResonanceBuilder import ResonanceBuilder
higgses_rescaled = cfg.Analyzer(
    ResonanceBuilder,
    output = 'higgses_rescaled',
    leg_collection = 'jets_rescaled',
    pdgid = 25
)

higgses = cfg.Analyzer(
    ResonanceBuilder,
    output = 'higgses',
    leg_collection = 'jets',
    pdgid = 25
)

# Just a basic analysis-specific event Selection module.
# this module implements a cut-flow counter
# After running the example as
#    heppy_loop.py Trash/ analysis_ee_ZH_cfg.py -f -N 100 
# this counter can be found in:
#    Trash/example/heppy.analyzers.examples.zh.selection.Selection_cuts/cut_flow.txt
# Counter cut_flow :
#         All events                                     100      1.00    1.0000
#         At least 2 leptons                              87      0.87    0.8700
#         Both leptons e>30                               79      0.91    0.7900
# For more information, check the code of the Selection class
# in heppy/analyzers/examples/zh/selection.py
from heppy.analyzers.examples.zh.selection import Selection
selection = cfg.Analyzer(
    Selection,
    instance_label='cuts'
)

# Analysis-specific ntuple producer
# please have a look at the code of the ZHTreeProducer class,
# in heppy/analyzers/examples/zh/ZHTreeProducer.py
from fcc_ee_higgs.analyzers.ZHTreeProducer import ZHTreeProducer
tree = cfg.Analyzer(
    ZHTreeProducer,
    jet_collections = ['jets', 'jets_rescaled'],
    resonances=['higgses', 'higgses_rescaled'], 
    misenergy = ['missing_energy', 'missing_energy_rescaled']
)

from heppy.analyzers.PDebugger import PDebugger
pdebug = cfg.Analyzer(
PDebugger,
output_to_stdout = False, #optional
debug_filename = os.getcwd()+'/python_physics_debug.log' #optional argument
)

# definition of a sequence of analyzers,
# the analyzers will process each event in this order
sequence = cfg.Sequence(
    source,
    papas_sequence,
    jets,
    missing_energy,
    jet_rescaling, 
    btag_parametrized,
    # bjets, 
    # onebjet,
    missing_energy_rescaled, 
    higgses,
    higgses_rescaled, 
    # selection, 
    tree,
    # display
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
