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
logging.basicConfig(level=logging.INFO)

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
Event.print_patterns=['gen_bosons', '*jets*', '*taus*', 'higgses', 'zedqqs']

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
# nfiles = sys.maxint
nfiles = 1
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
zhtautau = cfg.Component(
    'zhtautau',
    files=test_files, 
    splitFactor=len(test_files)
)

ztautau = cfg.Component(
    'ztautau',
    files='ee_Z.root', 
    splitFactor=len(test_files)
)

cpslist = [
    ww
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

# gen taus
from fcc_ee_higgs.analyzers.GenTauSelector import GenTauSelector
gen_taus = cfg.Analyzer(
    GenTauSelector, 
    gen_particles = 'gen_particles',
)

from heppy.analyzers.EventFilter import EventFilter
two_gen_taus_in_acceptance = cfg.Analyzer(
    EventFilter,
    input_objects='gen_taus_acc',
    min_number=2, 
    veto=False    
)

# gen bosons

from fcc_ee_higgs.analyzers.GenResonanceAnalyzer import GenResonanceAnalyzer
gen_bosons = cfg.Analyzer(
    GenResonanceAnalyzer,
    pdgids=[23, 24, 25],
    statuses=[62],
    # decay_pdgids=[11, 13],
    verbose=True
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
    fastjet_args = dict( R=0.2, p=-1, emin=5),
#     fastjet_args = dict( njets=4 ),
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

from fcc_ee_higgs.analyzers.TauSelector import TauSelector
from heppy.analyzers.Masker import Masker

taus = cfg.Analyzer(
    TauSelector,
    output='taus', 
    jets='jets',
    verbose=False
)

from heppy.analyzers.EventFilter import EventFilter
two_taus = cfg.Analyzer(
    EventFilter, 
    input_objects='taus',
    min_number=2, 
    veto=False
)

from heppy.analyzers.Matcher import Matcher
gen_tau_match = cfg.Analyzer(
    Matcher,
    delta_r = 0.3,
    particles = 'gen_taus', 
    match_particles = 'taus',
)

rec_tau_match = cfg.Analyzer(
    Matcher,
    delta_r = 0.3,
    particles = 'taus', 
    match_particles = 'gen_taus',
)

gen_tau_match = cfg.Analyzer(
    Matcher,
    delta_r = 0.3,
    particles = 'gen_taus', 
    match_particles = 'taus',
)

from fcc_ee_higgs.analyzers.QQTauTauAnalyzer2 import QQTauTauAnalyzer2
qqtautau = cfg.Analyzer(
    QQTauTauAnalyzer2,
    jets='jets',
    taus='taus',
    particles='rec_particles'
)

from fcc_ee_higgs.analyzers.TauTreeProducer import TauTreeProducer
tau_tree = cfg.Analyzer(
    TauTreeProducer,
    instance_label='rec', 
    taus='taus',
    
)

gen_tau_tree = cfg.Analyzer(
    TauTreeProducer,
    instance_label='gen', 
    taus='gen_taus',
    
)

# Analysis-specific ntuple producer
# please have a look at the code of the ZHTreeProducer class,
# in heppy/analyzers/examples/zh/ZHTreeProducer.py
from fcc_ee_higgs.analyzers.ZHTreeProducer import ZHTreeProducer
tree = cfg.Analyzer(
    ZHTreeProducer,
    jet_collections = ['bestjets', 'besttaus'],
    resonances=['higgs', 'higgs_r', 'zedqq2', 'zedqq2_r'], 
    misenergy = ['missing_energy'],
    particles=['zedqq'], 
)

# definition of a sequence of analyzers,
# the analyzers will process each event in this order
sequence = cfg.Sequence(
    source,
    gen_taus,
#    two_gen_taus_in_acceptance,
#    display, 
    gen_bosons, 
    papas_sequence,
##    leptons,
##    iso_leptons,
##    sel_iso_leptons,
##    zedlls,
##    leg_extractor, 
    missing_energy,
    jets,
    taus,
    two_taus,
    rec_tau_match, 
    tau_tree,
    gen_tau_match,
    gen_tau_tree, 
##    beta4rescaler,
##    taus_rescaled, 
    qqtautau, 
    tree,  
##    beta4rescaler, 
##    higgses,
##    jets_not_taus,
##    zedqqs,
##    taus_rescaled,
##    higgses_rescaled,
##    jets_not_taus_rescaled,
##    zedqqs_rescaled, 
    
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
