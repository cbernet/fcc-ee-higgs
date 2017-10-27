import os 
from fcc_datasets.fcc_component import FCCComponent
# import fcc_datasets.basedir as basedir
# basedir.basename = '/Users/cbernet/Datasets/FCC/fcc_ee_higgs/samples'

ZHnunu = FCCComponent(
    'heppy/ee_to_ZH_Z_to_nunu_H_to_bb/Oct23/pythia/ee_to_ZH_Z_to_nunu_Jun21_A_1',
    xSection=1.3e-11*3,
    nGenEvents=5000*100.
)

ZZ = FCCComponent(
    'heppy/ee_to_ZH_Z_to_nunu_H_to_bb/Oct23/pythia/ee_to_ZZ_Sep12_A_2',
    xSection=1.35e-9,
    nGenEvents=10000*200.
)

ffbar = FCCComponent(
    'heppy/ee_to_ZH_Z_to_nunu_H_to_bb/Oct23/pythia/ee_to_ffbar_Sep12_B_4',
    xSection=7.9e-8,
    nGenEvents=10000*500.
)
