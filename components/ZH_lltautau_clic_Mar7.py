import os 
from fcc_datasets.fcc_component import FCCComponent

ZH = FCCComponent(
    'heppy/ee_to_ZH_Z_to_lltautau/CLD/Mar7/ee_to_ZH_Oct30', 
    xSection=2.e-10,  
    nGenEvents=5000*100.,
    uncertainty=0.1    
)

ZZ = FCCComponent(
    'heppy/ee_to_ZH_Z_to_lltautau/CLD/Mar7/ee_to_ZZ_Sep12_A_2', 
    xSection=1.35e-9,  
    nGenEvents=10000*200.,
    uncertainty=0.05    
)

WW = FCCComponent(
    'heppy/ee_to_ZH_Z_to_lltautau/CLD/Mar7/ee_to_WW_Dec6_large',
    xSection=1.64e-8,  
    nGenEvents=20000*200.,
    uncertainty=0.05    
)

##ll = FCCComponent(
##    'heppy/ee_to_ZH_Z_to_lltautau/CLD/Mar7/ee_to_ffbar_2l_Mar6',
##    xSection=9.3e-9,  
##    nGenEvents=10000*97,
##    uncertainty=0.05    
##)

ll = FCCComponent(
    'heppy/ee_to_ZH_Z_to_lltautau/CLD/Mar8/ee_to_2l_Mar8',
    xSection=9.3e-9,  
    nGenEvents=20000*499,
    uncertainty=0.05    
)
