'''Example configuration file for an ee->ZH->mumubb analysis in heppy, with the FCC-ee

While studying this file, open it in ipython as well as in your editor to 
get more information: 

ipython
from analysis_ee_ZH_cfg import * 
'''

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
Event.print_patterns=['zeds*', 'higgs*', 'jets*', 'bquarks', 'recoil*', 'collections']

# definition of the collider
# help(Collider) for more information
from heppy.configuration import Collider
Collider.BEAMS = 'ee'
Collider.SQRTS = 240.

jet_correction = True

# mode = 'ee_to_ZH_Z_to_nunu_Jun21_A_1'
# mode = 'ee_to_ZZ_Sep12_A_2'
nfiles = 20
mode = 'test'

# definition of input samples                                                                                                   
# from components.ZH_Znunu import components as cps
from fcc_ee_higgs.components.all import load_components
cps = load_components(mode='pythia')

selectedComponents = cps.values()                                                                                      
for comp in selectedComponents:
    comp.splitFactor = len(comp.files)

test_filename = 'samples/test/ee_ZZ_nunu.root'
if mode == 'test':
    comp = cps['ee_to_ZZ_Sep12_A_2']
    comp.files = [test_filename]
    comp.splitFactor = 1
    selectedComponents = [comp]
elif mode == 'debug':
    comp = cfg.Component(
        'Debug',
        files=['ee_ffbar.root']
    )
    selectedComponents = [comp]
else:
    selectedComponents = [cps[mode]]
    if nfiles: 
        cps[mode].files = cps[mode].files[:nfiles]
    
# read FCC EDM events from the input root file(s)
# do help(Reader) for more information
from heppy.analyzers.fcc.Reader import Reader
source = cfg.Analyzer(
    Reader,
    gen_particles = 'GenParticle',
    gen_vertices = 'GenVertex'
)

# gen level filtering
lepton_id = 13
from heppy.analyzers.Selector import Selector
gen_leptons = cfg.Analyzer(
    Selector,
    'gen_leptons',
    output = 'gen_leptons',
    input_objects = 'gen_particles',
    filter_func = lambda ptc: ptc.e() > 5. and abs(ptc.pdgid()) == lepton_id
)

from heppy.analyzers.EventFilter   import EventFilter  
gen_counter = cfg.Analyzer(
    EventFilter  ,
    'gen_counter',
    input_objects = 'gen_leptons',
    min_number = 2,
    veto = False
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
from heppy.test.papas_cfg import papas, papas_sequence, detector

from heppy.test.papas_cfg import papasdisplaycompare as display 

# Use a Selector to select leptons from the output of papas simulation.
# Currently, we're treating electrons and muons transparently.
# we could use two different instances for the Selector module
# to get separate collections of electrons and muons
# help(Selector) for more information
leptons_true = cfg.Analyzer(
    Selector,
    'sel_leptons',
    output = 'leptons_true',
    input_objects = 'rec_particles',
    filter_func = lambda ptc: ptc.e()>10. and abs(ptc.pdgid()) in [11, 13]
)

# Compute lepton isolation w/r other particles in the event.
# help(IsolationAnalyzer) for more information
from heppy.analyzers.IsolationAnalyzer import IsolationAnalyzer
from heppy.particles.isolation import EtaPhiCircle
iso_leptons = cfg.Analyzer(
    IsolationAnalyzer,
    candidates = 'leptons_true',
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
    input_objects = 'leptons_true',
    # filter_func = relative_isolation
    filter_func = lambda lep : lep.iso.sumpt/lep.pt()<0.3 # fairly loose
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

zed_counter = cfg.Analyzer(
    EventFilter  ,
    'zed_counter',
    input_objects = 'zeds',
    min_number = 0,
    veto = False
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
    to_remove = 'zeds_legs'
) 

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

# Creating a list of particles excluding the decay products of the best zed.
# help(Masker) for more information
from heppy.analyzers.Masker import Masker
particles_not_zed = cfg.Analyzer(
    Masker,
    output = 'particles_not_zed',
    input = 'rec_particles',
    mask = 'zeds_legs',
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
)

# b tagging 
from heppy.test.btag_parametrized_cfg import btag_parametrized, btag
from heppy.analyzers.roc import cms_roc
btag.roc = cms_roc

def is_bjet(jet):
    return jet.tags['b'] == 1
    
bjets = cfg.Analyzer(
    Selector,
    'bjets',
    output = 'bjets',
    input_objects = 'jets',
    # filter_func=is_bjet, 
    filter_func = lambda jet: jet.tags['b'] == 1
)

onebjet = cfg.Analyzer(
    EventFilter  ,
    'onebjet',
    input_objects = 'bjets',
    min_number = 1,
    veto = False
)

# Build Higgs candidates from pairs of jets.
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
    jets = 'jets',
    jets_rescaled = 'jets_rescaled',
    higgs=['higgses', 'higgses_rescaled'], 
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
    #pdebug,
    # gen_leptons,
    # gen_counter,
    # gen_leptons, 
    # gen_ana, 
    papas_sequence,
    # leptons_true,
    # iso_leptons,
    # sel_iso_leptons,
    # zeds,
    # zed_counter, 
    # recoil,
    # particles_not_zed,
    ## jets_raw, 
    jets,
    missing_energy,
    jet_rescaling, 
    btag_parametrized,
    bjets, 
    # onebjet,
    missing_energy_rescaled, 
    higgses,
    higgses_rescaled, 
    # selection, 
    tree,
##    display
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
