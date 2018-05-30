process = 'ee_ZH_any'
'''
Adapted example
Example configuration file for an ee->ZH analysis in the 4 jet channel,
with the FCC-ee

While studying this file, open it in ipython as well as in your editor to 
get more information: 

ipython
from analysis_ee_ZH_had_cfg import * 

'''
PTMIN = 8
import os
import sys
import copy
import heppy.framework.config as cfg

from heppy.framework.event import Event
Event.print_patterns=['*jet*', 'bquarks', '*higgs*',  
                      '*zed*', '*lep*']

import logging
# next 2 lines necessary to deal with reimports from ipython
logging.shutdown()
reload(logging)
logging.basicConfig(level=logging.WARNING)

# setting the random seed for reproducible results
import heppy.statistics.rrandom as random
random.seed(0xdeadbeef)

# definition of the collider
from heppy.configuration import Collider
Collider.BEAMS = 'ee'
Collider.SQRTS = 240.

# mode = 'pythia/ee_to_ZH_Oct30'
mode = 'all'
nfiles = None

from fcc_datasets.fcc_component import FCCComponent

zh = FCCComponent( 
    'pythia/ee_to_ZH_Oct30',
    splitFactor=4
)

from fcc_ee_higgs.components.tools import get_components
selectedComponents = get_components(mode, [zh], nfiles)

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


# the papas simulation and reconstruction sequence
from heppy.test.papas_cfg import papas, pfreconstruct, papas_sequence
# from heppy.papas.detectors.FCCHiggsDetectors.config.cfg_CLIC import papas_sequence, detector, papas, gen_particles_stable
# on Detector change, change ROC curve!!!!
from heppy.papas.detectors.CLIC import clic as detector
papas.detector = detector    
pfreconstruct.detector = detector

# write out partons from Z and H decays
#from heppy.analyzers.mytest_PartonAnalyzer import PartonsFromZH
##from fcc_ee_higgs.analyzers.qqbb.PartonAnalyzer import PartonsFromZH
##partons = cfg.Analyzer(
##    PartonsFromZH,
##    partons = 'partons'
##)

# Use a Selector to select leptons from the output of papas simulation.
# Currently, we're treating electrons and muons transparently.
# we could use two different instances for the Selector module
# to get separate collections of electrons and muons
# help(Selector) for more information
from heppy.analyzers.Selector import Selector
def is_lepton(ptc):
    return ptc.e()> 5. and abs(ptc.pdgid()) in [11, 13]

leptons = cfg.Analyzer(
    Selector,
    'sel_leptons',
    output = 'leptons',
    input_objects = 'rec_particles',
    #input_objects = 'gen_particles_stable',
    filter_func = is_lepton 
)

# Compute lepton isolation w/r other particles in the event.
# help(IsolationAnalyzer) 
# help(isolation) 
# for more information
from heppy.analyzers.IsolationAnalyzer import IsolationAnalyzer
from heppy.particles.isolation import EtaPhiCircle
iso_leptons = cfg.Analyzer(
    IsolationAnalyzer,
    candidates = 'leptons',
    particles = 'rec_particles',
    #particles = 'gen_particles_stable',
    iso_area = EtaPhiCircle(0.4)
)

# Select isolated leptons with a Selector
def is_isolated(lep):
    '''returns true if the particles around the lepton
    in the EtaPhiCircle defined above carry less than 30%
    of the lepton energy.'''
    return lep.iso.sume/lep.e()<0.3  # fairly loose

sel_iso_leptons = cfg.Analyzer(
    Selector,
    'sel_iso_leptons',
    output = 'sel_iso_leptons',
    input_objects = 'leptons',
    filter_func = is_isolated
)

# make inclusive jets with pt>10GeV
from heppy.analyzers.fcc.JetClusterizer import JetClusterizer
jets_inclusive = cfg.Analyzer(
    ## Colin : inclusive jets
    JetClusterizer,
    output = 'jets_inclusive',
    particles = 'rec_particles',
    #particles = 'gen_particles_stable',
    fastjet_args = dict(R=0.4, p=-1, emin=5),  ##Colin replaced by lower E cut
)

# make inclusive gen jets with stable gen particles
##genjets = cfg.Analyzer(
##    ## Colin : inclusive jets, gen particles
##    JetClusterizer,
##    output = 'exgenjets',
##    particles = 'gen_particles_stable',
##    fastjet_args = dict(R=0.4, p=-1, emin=5),
##)

# count exclusive jets
##from fcc_ee_higgs.analyzers.qqbb.JetCounter import JetCounter
##jetcounter = cfg.Analyzer(
##    ### Colin : appends number of jets to the event
##    JetCounter,
##    input_jets = 'exjets',
##    njets = 'n_jets'
##)

from heppy.analyzers.EventFilter   import EventFilter  
jetcounter = cfg.Analyzer(
    EventFilter  ,
    'jetcounter',
    input_objects = 'jets_inclusive',
    min_number = 4,
    veto = False
)

##genjetcounter = cfg.Analyzer(
##    ### Colin : appends number of jets to the event
##    JetCounter,
##    input_jets = 'exgenjets',
##    njets = 'n_genjets'
##)

# make four exclusive jets
from heppy.analyzers.fcc.JetClusterizer import JetClusterizer
jets_exclusive = cfg.Analyzer(
    JetClusterizer,
    output = 'jets',
    particles = 'rec_particles',
    #particles = 'gen_particles_stable',
    fastjet_args = dict(njets=4)  
)

# make four inclusive gen jets with stable gen particles
##inclgenjets = cfg.Analyzer(
##    ## Colin : same with gen 
##    JetClusterizer,
##    output = 'genjets',
##    particles = 'gen_particles_stable',
##    fastjet_args = dict(njets=4)  
##)

#reject Z decays into Leptons
##from fcc_ee_higgs.analyzers.qqbb.RejectZLeptonic import RejectZLeptonic
##reject_Z_leptonic = cfg.Analyzer(
##    ## Colin : does not reject, just keep track of number of particles
##    ## and number of charged hadrons
##    ## adds ljets to the event, but the same as jets
##    RejectZLeptonic,
##    input_jets = 'jets',
##    output_jets = 'ljets'
##)

from heppy.analyzers.Tagger import Tagger
jet_tagger = cfg.Analyzer(
    Tagger,
    input_objects='jets',
    tags = dict(
      n_constituents=lambda x: x.constituents.n_particles(),
      n_charged_hadrons=lambda x: x.constituents.n_charged_hadrons(),
      is_photon=lambda x: x.constituents[22].e()/x.e()>0.95
    )
)

# rescale the jet energy taking according to initial p4
from fcc_ee_higgs.analyzers.qqbb.JetEnergyComputer import JetEnergyComputer
compute_jet_energy = cfg.Analyzer(
    ## Colin rescale the jets. looks like beta4
    ## warning: original jets probably modified
    JetEnergyComputer,
    output_jets='rescaled_jets',
    out_chi = 'chi2',
    input_jets='jets',
    sqrts=Collider.SQRTS
)

# select b quarks for jet to parton matching.
##def is_outgoing_quark(ptc):
##    '''returns True if the particle is an outgoing b quark,
##    see
##    http://home.thep.lu.se/~torbjorn/pythia81html/ParticleProperties.html
##    '''
##    return abs(ptc.pdgid()) <= 6 and ptc.status() == 23
##    
##outgoing_quarks = cfg.Analyzer(
##    Selector,
##    'outgoing_quarks',
##    output = 'outgoing_quarks',
##    input_objects = 'gen_particles',
##    filter_func =is_outgoing_quark
##)

# match genjets to b quarks 
##from heppy.analyzers.Matcher import Matcher
##genjet_to_b_match = cfg.Analyzer(
##    Matcher,
##    match_particles = 'outgoing_quarks',
##    particles = 'genjets',
##    delta_r = 0.4 #default 0.4
##    )

# match jets to genjets (so jets are matched to b quarks through gen jets)
##jet_to_genjet_match = cfg.Analyzer(
##    Matcher,
##    match_particles='genjets',
##    particles='rescaled_jets',
##    delta_r=0.5
##)

#Reject events that are compatible with a fully hadronic ZZ or WW decay
from fcc_ee_higgs.analyzers.qqbb.FullHadCompatible import FullHadCompatible
fullhadcompatible = cfg.Analyzer(
    FullHadCompatible,
    input_jets='rescaled_jets',
    output_jets='hjets',
    dWW = 'deltaWW',
    dZZ = 'deltaZZ',
    pair1_m = 'm12',
    pair2_m = 'm34'
)

from heppy.analyzers.ParametrizedBTagger import ParametrizedBTagger
from heppy.analyzers.roc import ROC
import numpy as np
clic_roc = ROC(
    np.array([
       [1e-9, 1e-9],
       [0.8, 4e-3]
   ])
)

clic_roc.set_working_point(0.8)
btag = cfg.Analyzer(
    ParametrizedBTagger,
#    input_jets='hjets',
    input_jets='jets',
    roc=clic_roc
)

# pt-dependend b tagging, also based on CMS-performance
# different efficiencies for b, c and other quarks.
##from fcc_ee_higgs.analyzers.qqbb.BTagger import BTagger
##btag_pt = cfg.Analyzer(
##    BTagger,
##    input_jets = 'hjets',
##)

from heppy.analyzers.Selector import Selector
bjets = cfg.Analyzer(
    Selector,
    'bjets',
    output = 'bjets',
    input_objects = 'jets',
    filter_func = lambda jet: jet.tags['b']
)

two_bjets = cfg.Analyzer(
    EventFilter,
    'two_bjets',
    input_objects='bjets',
    min_number=2,
    veto=False
)

# compute the missing 4-momentum
from heppy.analyzers.RecoilBuilder import RecoilBuilder
missing_energy = cfg.Analyzer(
    RecoilBuilder,
    instance_label = 'missing_energy',
    output = 'missing_energy',
    sqrts = Collider.SQRTS,
    to_remove = 'rec_particles'
    #to_remove = 'gen_particles_stable'
) 

from heppy.analyzers.P4SumBuilder import P4SumBuilder
sum_vis = cfg.Analyzer(
    P4SumBuilder,
    output = 'sum_vis',
    particles = 'rec_particles',
) 



#Find the Particle (H, Z, ...) from which the jets originate
##from fcc_ee_higgs.analyzers.qqbb.AncestorSeeker import AncestorSeeker
##ancestors = cfg.Analyzer(
##    AncestorSeeker,
##    input_jets = 'genjets'
##)

##from fcc_ee_higgs.analyzers.qqbb.MatchTransfer import MatchTransfer
##matchtransfer = cfg.Analyzer(
##    MatchTransfer,
##    input_jets = 'hjets',
##    input_genjets = 'genjets'
##)

# reconstruction of the H and Z resonances.
# for now, use for the Higgs the two b jets with the mass closest to mH
# the other 2 jets are used for the Z.
# implement a chi2? 
from fcc_ee_higgs.analyzers.qqbb.ZHReconstruction import ZHReconstruction
zhreco = cfg.Analyzer(
    ZHReconstruction,
    output_higgs='higgs',
    output_zed='zed', 
    input_jets='hjets',
    numberOfCandidates = 'n_candidates',
    higgsmass='higgsmass', #Ausgabe der Higgsmasse nach der Formel aus dem Paper
    mHJet = 'mHJet',
    mZedJet = 'mZedJet',
    anc1 = 'higgs_anc1',
    anc2 = 'higgs_anc2',
    log_level=logging.INFO    
)

# simple cut flow printout
from fcc_ee_higgs.analyzers.qqbb.FinalSelection import FinalSelection
selection = cfg.Analyzer(
    FinalSelection,
##    njets = 'n_jets',
##    rawjets='jets',
##    # cutjets='cjets',
##    # leptonjets='ljets',
##    # massjets='ejets',
##    # hadjets='hjets',
##    input_jets='hjets', 
##    vismass = 'vismass',
##    dWW = 'deltaWW',
##    dZZ = 'deltaZZ',
##    mHJet = 'mHJet',
##    mZedJet = 'mZedJet',
##    higgs='higgs',
##    higgsmass='higgsmass', 
##    anc1 = 'higgs_anc1',
##    anc2 = 'higgs_anc2',
##    zed='zed',
##    leptons='sel_iso_leptons',
##    numberOfCandidates = 'n_candidates',
##    chi2 = 'chi2',
    log_level=logging.INFO
)

from fcc_ee_higgs.analyzers.qqbb.BaseSelection import BaseSelection
base_cut_flow = cfg.Analyzer(
    BaseSelection, 
    log_level=logging.INFO
)

# Analysis-specific ntuple producer
# please have a look at the ZHTreeProducer class
from fcc_ee_higgs.analyzers.qqbb.QQBBTreeProducer import QQBBTreeProducer
tree = cfg.Analyzer(
    QQBBTreeProducer,
    misenergy = 'missing_energy', 
    rawjets='jets',
#    cutjets = 'cjets',
    leptonjets = 'ljets',
    massjets = 'ejets',
    rejets = 'rescaled_jets',
    chi2 = 'chi2',
    hadjets = 'hjets',
    genjets='genjets',
    vismass = 'vismass',
    dWW = 'deltaWW',
    dZZ = 'deltaZZ',
    pair1_m = 'm12',
    pair2_m = 'm34',
    mHJet = 'mHJet',
    mZedJet = 'mZedJet',
    higgs='higgs',
    higgsmass='higgsmass', 
    anc1 = 'higgs_anc1',
    anc2 = 'higgs_anc2',
    zed='zed',
    leptons='sel_iso_leptons',
    numberOfCandidates = 'n_candidates',
    njets = 'n_jets',
    ngenjets = 'n_genjets'
)

# definition of the sequence of analyzers,
# the analyzers will process each event in this order
sequence = cfg.Sequence(
    source,
    gen_bosons, 
    papas_sequence,
    #gen_particles_stable, # need to include this only if papas_sequence is excluded
#    partons,
    leptons,
    iso_leptons,
    sel_iso_leptons,
#    lepton_veto, 
#    genjets, 
#    genjetcounter,
    missing_energy,
    sum_vis, 
    jets_inclusive,
    jetcounter,
    jets_exclusive,
    btag,
    bjets,
#    inclgenjets,
#    reject_Z_leptonic,
    jet_tagger, 
#    reject_missing_nrg,
    compute_jet_energy, 
#    outgoing_quarks,
#    genjet_to_b_match,
#    jet_to_genjet_match, 
#    ancestors,
    base_cut_flow, 
    two_bjets, 
    fullhadcompatible,
#    btag_pt,
#    matchtransfer,
    zhreco, 
    selection, 
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
