import os 
from fcc_datasets.fcc_component import FCCComponent

# mode = 'no_beam_smearing_new'
# mode = 'isofix'
mode = 'isofix_bs' 

# For ZH, ZZ, WW, there is a cut E>10 on reconstructed leptons! 
ZH = FCCComponent(
    'heppy/ee_to_ZH_to_llww/CLD/May23/ee_to_ZH_Oct30', 
    xSection=2.e-10,  
    nGenEvents=5000*100.,
    uncertainty=0.2    
)

ZH_bs = FCCComponent(
    'heppy/ee_to_ZH_to_llww/CLD/ee_to_ZH_BS_je5_Oct2', 
    xSection=2.e-10,  
    nGenEvents=5000*100.,
    uncertainty=0.2    
)

ZH_nobs_new = FCCComponent(
    'heppy/ee_to_ZH_to_llww/CLD/ee_to_ZH_Oct30', 
    xSection=2.e-10,  
    nGenEvents=5000*100.,
    uncertainty=0.2    
)

ZH_isofix = FCCComponent(
    'heppy/ee_to_ZH_to_llww/CLD/IsoFix/ee_to_ZH_Oct30', 
    xSection=2.e-10,  
    nGenEvents=5000*100.,
    uncertainty=0.2    
)

ZH_isofix_bs = FCCComponent(
    'heppy/ee_to_ZH_to_llww/CLD/IsoFix/ee_to_ZH_BS_Oct2', 
    xSection=2.e-10,  
    nGenEvents=5000*100.,
    uncertainty=0.2    
)

ZZ = FCCComponent(
    'heppy/ee_to_ZH_to_llww/CLD/May23/ee_to_ZZ_Sep12_A_2', 
    xSection=1.35e-9,  
    nGenEvents=10000*200.,
    uncertainty=0.2    
)

ZZ_bs = FCCComponent(
    'heppy/ee_to_ZH_to_llww/CLD/ee_to_ZZ_BS_je5_Oct2', 
    xSection=1.35e-9,  
    nGenEvents=10000*200.,
    uncertainty=0.2    
)

ZZ_nobs_new = FCCComponent(
    'heppy/ee_to_ZH_to_llww/CLD/ee_to_ZZ_Sep12_A_2', 
    xSection=1.35e-9,  
    nGenEvents=10000*199.,
    uncertainty=0.2    
)

ZZ_isofix = FCCComponent(
    'heppy/ee_to_ZH_to_llww/CLD/IsoFix/ee_to_ZZ_Sep12_A_2', 
    xSection=1.35e-9,  
    nGenEvents=10000*199.,
    uncertainty=0.2    
)

ZZ_isofix_bs = FCCComponent(
    'heppy/ee_to_ZH_to_llww/CLD/IsoFix/ee_to_ZZ_BS_Oct2', 
    xSection=1.35e-9,  
    nGenEvents=10000*199.,
    uncertainty=0.2    
)


WW = FCCComponent(
    'heppy/ee_to_ZH_to_llww/CLD/May23/ee_to_WW_Dec6_large',
    xSection=1.64e-8,  
    nGenEvents=20000*200.,
    uncertainty=0.2    
)

WW_isofix = FCCComponent(
    'heppy/ee_to_ZH_to_llww/CLD/IsoFix/ee_to_WW_Dec6_large',
    xSection=1.64e-8,  
    nGenEvents=20000*200.,
    uncertainty=0.2    
)


ll = FCCComponent(
    # cut on lepton energy ok
    'heppy/ee_to_ZH_to_llww/CLD/May23/ee_to_2l_Mar8',
    xSection=9.3e-9,  
    nGenEvents=20000*498,
    uncertainty=0.2    
)

ll_isofix = FCCComponent(
    # cut on lepton energy ok
    'heppy/ee_to_ZH_to_llww/CLD/IsoFix/ee_to_2l_Mar8',
    xSection=9.3e-9,  
    nGenEvents=20000*498,
    uncertainty=0.2    
)


if mode == 'beam_smearing':
    ZH = ZH_bs
    ZZ = ZZ_bs
elif mode == 'no_beam_smearing_new':
    ZH = ZH_nobs_new
    ZZ = ZZ_nobs_new
elif mode == 'isofix':
    ZH = ZH_isofix
    ZZ = ZZ_isofix
    WW = WW_isofix
    ll = ll_isofix
elif mode == 'isofix_bs':
    ZH = ZH_isofix_bs
    ZZ = ZZ_isofix_bs
    WW = WW_isofix
    ll = ll_isofix
    
