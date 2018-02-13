import os 
from fcc_datasets.fcc_component import FCCComponent
# import fcc_datasets.basedir as basedir
# basedir.basename = '/Users/cbernet/Datasets/FCC/fcc_ee_higgs/samples'

ZH = FCCComponent(
    'heppy/ee_to_ZH_Z_to_nunu_H_to_bb/Dec12/ee_to_ZH_Oct30',
    xSection=2.e-10,
    nGenEvents=5000*100.,
    uncertainty=0.1
)

ZZ = FCCComponent(
    '/heppy/ee_to_ZH_Z_to_nunu_H_to_bb/Dec12/ee_to_ZZ_Sep12_A_2',
    xSection=1.35e-9,
    nGenEvents=10000*200.,
    uncertainty=0.1
)

ffbar = FCCComponent(
    'heppy/ee_to_ZH_Z_to_nunu_H_to_bb/Dec12/ee_to_ffbar_Sep12_B_4',
    xSection=7.9e-8,
    nGenEvents=10000*500.,
    uncertainty=0.1
)

WW = FCCComponent(
    'heppy/ee_to_ZH_Z_to_nunu_H_to_bb/Dec12/ee_to_WW_Dec6_large',
    xSection=1.6e-8,
    nGenEvents=20000*195.,
    uncertainty=0.1
)
