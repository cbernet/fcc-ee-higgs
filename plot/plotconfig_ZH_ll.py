var = 'recoil_m'
# xtitle = 'm_{Recoil} (GeV)'
xtitle = 'm_{H} (GeV)'

# channel = 'bb'
channel = 'inclusive'
# channel = 'tautau'

detector = 'CLIC-FCCee'
# detector = 'CMS'
lumi = 500e12

# bins = 100, 50, 150
bins = 50, 50, 150

def get_cut_hbb(eff, fake, operator='||'):
    return '(((jets_1_bmatch==1 && rndm<{eff}) || (jets_1_bmatch==0 && rndm<{fake})) {op} \
((jets_2_bmatch==1 && rndm<{eff}) || (jets_2_bmatch==0 && rndm<{fake})))'.format(eff=eff, fake=fake, op=operator)

if detector is 'CMS':
    from fcc_ee_higgs.components.ZH_Zll import ZH, ZZ, WW
    b_wp = (0.6, 3e-3)    
elif detector is 'CLIC-FCCee':
    from fcc_ee_higgs.components.ZH_Zll_clic import ZH, ZZ, WW
    b_wp = (0.8, 4e-3)
    # b_wp = (1., 0)
comps = [ZZ, ZH, WW]
ZH.name =  'ZH'
ZZ.name =  'ZZ'
WW.name =  'WW'
from fcc_ee_higgs.components.tools import load
load(comps)    
cut_leps = '(zeds_1_iso_e/zeds_1_e<0.2) && (zeds_1_iso_e/zeds_1_e<0.2) && zeds_1_e>0 && zeds_2_e>0'
cut_z = '(abs(zeds_m-91)<4. && zeds_pt>10 && zeds_pz<50 && zeds_acol>100 && zeds_cross>10) && (zeds_1_pdgid==-zeds_2_pdgid) '
cut_rad = '((jets_1_e<0 || jets_1_22_e/jets_1_e<0.8) && \
(jets_2_e<0 || jets_2_22_e/jets_2_e<0.8))'
cut_hbb = get_cut_hbb(b_wp[0], b_wp[1], ' || ')
cut_htautau = '(((jets_1_211_num+jets_1_11_num+jets_1_13_num)==1 || (jets_1_211_num+jets_1_11_num+jets_1_13_num)==3) && \
((jets_2_211_num+jets_2_11_num+jets_2_13_num)==1 || (jets_2_211_num+jets_2_11_num+jets_2_13_num)==3))'
# cut_htautau = '((jets_1_211_num<=3) && (jets_2_211_num<=3))'

cut_hinv = '(jets_1_e<0 && jets_2_e<0)'
cut_hvis = '(jets_1_e>0 && jets_2_e>0)'

cut_Z = ' && '.join([cut_leps, cut_z, cut_rad])

cut = cut_Z
if channel is 'bb':
    cut = ' && '.join([cut_Z, cut_hbb])
