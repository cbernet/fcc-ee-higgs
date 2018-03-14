var = 'higgses_m'
# var = 'zeds_m'
xtitle = 'm_{H} (GeV)'

channel = 'qqtautau'

detector = 'CLD'
lumi = 500e12

bins = 50, 50, 150

##from fcc_ee_higgs.components.ZH_lltautau_clic_Mar2 import ZH, ZZ
##comps = [ZZ, ZH]
##ZH.name =  'ZH'
##ZZ.name =  'ZZ'

from fcc_ee_higgs.components.ZH_qqtautau_clic_Mar13 import ZH, ZZ, WW
comps = [ZZ, ZH, WW]
ZH.name =  'ZH'
ZZ.name =  'ZZ'
WW.name = 'WW'
##ll.name = 'll'
# ffbar.name = 'ffbar'
##
from fcc_ee_higgs.components.tools import load
load(comps)

from fcc_ee_higgs.plot.cuts import Cuts

cut_zqq = 'zedqqs_m>89 && zedqqs_m<100'
cut_htautau = '(((besttaus_1_211_num+besttaus_1_11_num+besttaus_1_13_num)==1 || (besttaus_1_211_num+besttaus_1_11_num+besttaus_1_13_num)==3) && \
 ((besttaus_2_211_num+besttaus_2_11_num+besttaus_2_13_num)==1 || (besttaus_2_211_num+besttaus_2_11_num+besttaus_2_13_num)==3))'
cut_htautau_1prong = '(((besttaus_1_211_num+besttaus_1_11_num+besttaus_1_13_num)==1) && \
 ((besttaus_2_211_num+besttaus_2_11_num+besttaus_2_13_num)==1))'
cut_zqq_jets = '(bestjets_1_m>1.5 && bestjets_2_m>1.5)'
cut_tau1_l = '((besttaus_1_11_num==1 || besttaus_1_13_num==1) && besttaus_1_211_num==0)'
cut_tau2_l = '((besttaus_2_11_num==1 || besttaus_2_13_num==1) && besttaus_2_211_num==0)'
cut_zedll = '!({}) && !({})'.format(cut_tau1_l, cut_tau2_l)
cut_zedll_2 = '(!(besttaus_1_11_num==1 && besttaus_2_11_num==1) && !(besttaus_1_13_num==1 && besttaus_2_13_num==1))'

##cut_htautau_or = '(((jets_1_211_num+jets_1_11_num+jets_1_13_num)==1 || (jets_1_211_num+jets_1_11_num+jets_1_13_num)==3) || \
## ((jets_2_211_num+jets_2_11_num+jets_2_13_num)==1 || (jets_2_211_num+jets_2_11_num+jets_2_13_num)==3))'
##cut_htautau_1 = '((jets_1_211_num+jets_1_11_num+jets_1_13_num)==1 || (jets_1_211_num+jets_1_11_num+jets_1_13_num)==3)'
##cut_missm = 'missing_energy_m/recoil_m<0.8'
##cut_rm4l = '!((second_zeds_1_pdgid==-second_zeds_2_pdgid) && (abs(second_zeds_1_pdgid)==13 || abs(second_zeds_1_pdgid)==11))'
##cut_leppt = '(zeds_1_pt>10 && zeds_2_pt>10)'

cuts = Cuts([
    ('cut_zqq', cut_zqq), 
    ('cut_htautau_1prong', cut_htautau_1prong),
    ('cut_zqqs_acol', 'zedqqs_acol>108'), 
    ('cut_zqq_jets', cut_zqq_jets),
    # ('cut_zedll', cut_zedll)
    ('cut_zedll_2', cut_zedll_2)
    # ('cut_htautau_or', cut_htautau_or),  
    # gain in precision! to investigate: try an or- nice but contamination is large of course...
##    ('cut_rm4l', cut_rm4l)
])

cut = str(cuts)

cut_gen_htautau = 'abs(genboson2_1_pdgid)==15'
cut_gen_hww = 'abs(genboson2_1_pdgid)==24'
cut_gen_hbb = 'abs(genboson2_1_pdgid)==5'
