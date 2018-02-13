import os 
from fcc_datasets.fcc_component import FCCComponent

ZH = FCCComponent(
    'heppy/ee_to_ZH_Z_to_ll/CMS/Jan30/ee_to_ZH_Oct30', 
    xSection=2.e-10,  
    nGenEvents=5000*98.,
    uncertainty=0.1
)

ZZ = FCCComponent(
    'heppy/ee_to_ZH_Z_to_ll/CMS/Jan30/ee_to_ZZ_Sep12_A_2', 
    xSection=1.35e-9,  
    nGenEvents=10000*198.,
    uncertainty=0.05
)

WW = FCCComponent(
    'heppy/ee_to_ZH_Z_to_ll/CMS/Jan30/ee_to_WW_Dec6_large', 
    xSection=1.64e-8,  
    nGenEvents=20000*197.,
    uncertainty=0.05
)



##ffbar = FCCComponent(
##    'heppy/ee_to_ZH_Z_to_nunu_H_to_bb/Oct23/pythia/ee_to_ffbar_Sep12_B_4',
##    xSection=7.9e-8,
##    nGenEvents=10000*500.
##)
