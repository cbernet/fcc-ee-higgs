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

ffbar2l = FCCComponent( 
    'pythia/ee_to_2l_Mar8',
    splitFactor=1
)

import glob
test_files=glob.glob('ee_ZH_Htautau.root')
zhtautau = cfg.Component(
    'zhtautau',
    files=test_files, 
    splitFactor=len(test_files)
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

from fcc_ee_higgs.analyzers.BeamSmearer import BeamSmearer

beam_smearer = cfg.Analyzer(
    BeamSmearer,
    # sigma=1.65e-3,
    sigma=0.1, 
    gen_particles='gen_particles'
)

# definition of a sequence of analyzers,
# the analyzers will process each event in this order
sequence = cfg.Sequence(
    source,
    beam_smearer
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
