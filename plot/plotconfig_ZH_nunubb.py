from fcc_ee_higgs.plot.plotconfig_ZH_ll import cut_hbb, bins, detector, lumi, xtitle

var = 'higgses_rescaled_m'
# var = 'missing_energy_m'

channel = 'nunubb'

if detector == 'CMS':
    from fcc_ee_higgs.components.ZH_nunubb import ZH, ZZ, WW, ffbar
    WW.name = 'WW'
    comps = [ZZ, ZH]
elif detector == 'CLD':
    from fcc_ee_higgs.components.ZH_nunubb_CLD_May17 import ZH, ZZ, ffbar, WW, WWH
    comps = [ZZ, ZH, ffbar, WW, WWH]
ZH.name =  'ZH'
WWH.name = 'WWH'
ZZ.name =  'ZZ'
ffbar.name =  'ffbar'
WW.name = 'WW'
from fcc_ee_higgs.components.tools import load
load(comps)

from fcc_ee_higgs.plot.cuts import Cuts

cut_missmass= '(missing_energy_m>87. && missing_energy_m<130.)' 
cut_h_pz = '(abs(missing_energy_pz)<50.)'
cut_h_pt = '(missing_energy_pt>10.)'
cut_h_acol = '(higgses_acol>100.)'
cut_h_cross = '(higgses_cross>10.)'
cut_ffbar_gamma = '(jets_1_22_e/jets_1_e<0.9 && jets_2_22_e/jets_2_e<0.9)'
cut_ffbar_e = '(jets_1_11_e/jets_1_e<0.9 && jets_2_11_e/jets_2_e<0.9)'
cut_ffbar_mu = '(jets_1_13_e/jets_1_e<0.9 && jets_2_13_e/jets_2_e<0.9)'
cut_ffbar_hpm = '(jets_1_211_num>3. && jets_2_211_num>3.)'

cuts = Cuts([
    ('cut_hbb', cut_hbb), 
    ('cut_h_pz', cut_h_pz), 
    ('cut_h_pt', cut_h_pt), 
    ('cut_h_acol', cut_h_acol), 
    ('cut_h_cross', cut_h_cross),
    ('cut_missmass', cut_missmass),
    ('cut_ffbar_hpm', cut_ffbar_hpm),
##    ('cut_ffbar_gamma', cut_ffbar_gamma), 
##    ('cut_ffbar_e', cut_ffbar_e), 
##    ('cut_ffbar_mu', cut_ffbar_mu), 
]
)

if var == 'missing_energy_m':
    del cuts['cut_missmass']

cut = str(cuts)
