var = 'higgs_r_m'
# var = 'zeds_m'
xtitle = 'm_{H} (GeV)'

channel = 'qqtautau'

detector = 'CLD'
lumi = 5000e12

bins = 50, 50, 150

##from fcc_ee_higgs.components.ZH_lltautau_clic_Mar2 import ZH, ZZ
##comps = [ZZ, ZH]
##ZH.name =  'ZH'
##ZZ.name =  'ZZ'

from fcc_ee_higgs.components.ZH_qqtautau_clic_Mar16 import ZH, ZZ, WW
comps = [ZZ, ZH, WW]
ZH.name =  'ZH'
ZZ.name =  'ZZ'
WW.name = 'WW'
from template import flatten
WW.preprocess = flatten
# WW.smooth = 1
##ll.name = 'll'
# ffbar.name = 'ffbar'
##
from fcc_ee_higgs.components.tools import load
load(comps)

vars = dict(
    bestjets_1_num = 'bestjets_1_211_num+bestjets_1_22_num+bestjets_1_22_num',
    bestjets_2_num = 'bestjets_1_211_num+bestjets_1_22_num+bestjets_1_22_num',
)    
for comp in comps:
    for alias, varstr in vars.iteritems():
        comp.tree.SetAlias(alias, varstr)
    
from fcc_ee_higgs.plot.cuts import Cuts
cut_zqq = '(zedqq2_r_m>75 && zedqq2_r_m<110)'
# cut_zqq = 'zedqq2_r_m>70 && zedqq2_r_m<110'
cut_zqq_acol = 'zedqq2_r_acol>110'
cut_zqq_acol_2 = 'zedqq2_acol>110'
cut_htautau = '(((besttaus_1_211_num+besttaus_1_11_num+besttaus_1_13_num)==1 || (besttaus_1_211_num+besttaus_1_11_num+besttaus_1_13_num)==3) && \
 ((besttaus_2_211_num+besttaus_2_11_num+besttaus_2_13_num)==1 || (besttaus_2_211_num+besttaus_2_11_num+besttaus_2_13_num)==3))'
cut_htautau_1prong = '(((besttaus_1_211_num+besttaus_1_11_num+besttaus_1_13_num)==1) && \
 ((besttaus_2_211_num+besttaus_2_11_num+besttaus_2_13_num)==1))'
cut_zqq_jets = '(bestjets_1_m>1.5 && bestjets_2_m>1.5)'
cut_tau1_l = '((besttaus_1_11_num==1 || besttaus_1_13_num==1) && besttaus_1_211_num==0)'
cut_tau2_l = '((besttaus_2_11_num==1 || besttaus_2_13_num==1) && besttaus_2_211_num==0)'
cut_zedll = '!({}) && !({})'.format(cut_tau1_l, cut_tau2_l)
cut_zedll_2 = '(!(besttaus_1_11_num==1 && besttaus_2_11_num==1) && !(besttaus_1_13_num==1 && besttaus_2_13_num==1))'
cut_zqq_2_WW = 'zedqq2_m>80'
cut_jete_WW = 'bestjets_1_e<80.'
cut_jetn_WW = '1'
cut_zqq_acop = 'zedqq2_acop>5'
cut_tau_iso = '((besttaus_1_iso_e/besttaus_1_e<0.05) && (besttaus_2_iso_e/besttaus_2_e<0.05))'

##cut_htautau_or = '(((jets_1_211_num+jets_1_11_num+jets_1_13_num)==1 || (jets_1_211_num+jets_1_11_num+jets_1_13_num)==3) || \
## ((jets_2_211_num+jets_2_11_num+jets_2_13_num)==1 || (jets_2_211_num+jets_2_11_num+jets_2_13_num)==3))'
##cut_htautau_1 = '((jets_1_211_num+jets_1_11_num+jets_1_13_num)==1 || (jets_1_211_num+jets_1_11_num+jets_1_13_num)==3)'
##cut_missm = 'missing_energy_m/recoil_m<0.8'
##cut_rm4l = '!((second_zeds_1_pdgid==-second_zeds_2_pdgid) && (abs(second_zeds_1_pdgid)==13 || abs(second_zeds_1_pdgid)==11))'
##cut_leppt = '(zeds_1_pt>10 && zeds_2_pt>10)'
cut_gen_htautau = 'abs(genboson2_1_pdgid)==15'
cut_gen_hww = 'abs(genboson2_1_pdgid)==24'
cut_gen_hbb = 'abs(genboson2_1_pdgid)==5'

cuts = Cuts([
    ('cut_zqq', cut_zqq),
    # ('cut_htautau', cut_htautau), 
    ('cut_htautau_1prong', cut_htautau_1prong),
    ('cut_zqq_acol', cut_zqq_acol), 
    ('cut_zqq_acol_2', cut_zqq_acol_2),
    ('cut_zqq_2_WW', cut_zqq_2_WW), 
    ('cut_zqq_jets', cut_zqq_jets),
    # ('cut_zedll', cut_zedll)
    ('cut_zedll_2', cut_zedll_2),
    ('cut_tau_iso', cut_tau_iso), 
    # ('cut_zqq_acop', cut_zqq_acop)
    # ('cut_jete_WW', cut_jete_WW)
    # ('cut_jetn_WW', cut_jetn_WW)
    # ('cut_gen_htautau', cut_gen_htautau)
    # ('cut_htautau_or', cut_htautau_or),  
    # gain in precision! to investigate: try an or- nice but contamination is large of course...
])

cut = str(cuts)


