import os 
from fcc_datasets.fcc_component import FCCComponent

# For ZH, ZZ, WW, there is a cut E>10 on reconstructed leptons! 
ZH = FCCComponent(
    'heppy/ee_to_ZH_to_qqwwll/CLD/Jun7/ee_to_ZH_Oct30', 
    xSection=2.e-10,  
    nGenEvents=5000*100.,
    uncertainty=0.2    
)

ZZ = FCCComponent(
    'heppy/ee_to_ZH_to_qqwwll/CLD/Jun7/ee_to_ZZ_Sep12_A_2', 
    xSection=1.35e-9,  
    nGenEvents=10000*200.,
    uncertainty=0.2    
)

WW = FCCComponent(
    'heppy/ee_to_ZH_to_qqwwll/CLD/Jun7/ee_to_WW_Dec6_large',
    xSection=1.64e-8,  
    nGenEvents=20000*200.,
    uncertainty=0.2    
)

ll = FCCComponent(
    # cut on lepton energy ok
    'heppy/ee_to_ZH_to_qqwwll/CLD/Jun7/ee_to_2l_Mar8',
    xSection=9.3e-9,  
    nGenEvents=20000*378,
    uncertainty=0.2    
)
