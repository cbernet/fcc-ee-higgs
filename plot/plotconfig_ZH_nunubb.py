from fcc_ee_higgs.plot.plotconfig_ZH_ll import cut_hbb, bins, detector, lumi, xtitle

var = 'higgses_rescaled_m'

channel = '0'

if detector == 'CMS':
    from fcc_ee_higgs.components.ZH_nunubb import ZH, ZZ, WW, ffbar
    WW.name = 'WW'
    comps = [ZZ, ZH]
elif detector == 'CLIC-FCCee':
    from fcc_ee_higgs.components.ZH_nunubb_clic import ZH, ZZ, ffbar
    comps = [ZZ, ZH, ffbar]
ZH.name =  'ZH' 
ZZ.name =  'ZZ'
ffbar.name =  'ffbar'    
from fcc_ee_higgs.components.tools import load
load(comps)

cut_missmass= 'missing_energy_m>85 && missing_energy_m<125'  # reoptimized cut
cut_h_pz = 'abs(missing_energy_pz)<50'
cut_h_pt = 'missing_energy_pt>15'
cut_h_acol = 'higgses_acol>100.'
cut_h_cross = 'higgses_cross>10'
all_cuts = [cut_missmass, cut_hbb, cut_h_pz, cut_h_pt, cut_h_acol, cut_h_cross]
cut = ' && '.join(all_cuts)

