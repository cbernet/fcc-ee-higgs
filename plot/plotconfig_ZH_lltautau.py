var = 'recoil_m'
# var = 'sel_zeds_m'
# var = 'higgses_r_m - recoil_m'

xtitle = 'm_{H} (GeV)'

channel = 'tautau'

detector = 'CLD'
lumi = 5000e12

bins = 50, 50, 150

def get_cut_hbb(eff, fake, operator='||'):
    return '(((jets_1_bmatch==1 && rndm<{eff}) || (jets_1_bmatch==0 && rndm<{fake})) {op} \
((jets_2_bmatch==1 && rndm<{eff}) || (jets_2_bmatch==0 && rndm<{fake})))'.format(eff=eff, fake=fake, op=operator)

b_wp = (0.8, 4e-3)

from fcc_ee_higgs.components.ZH_lltautau_clic_Mar26 import ZH, ZZ, ll, WW
comps = [ZZ, ZH, ll, WW]
ZH.name =  'ZH'
ZZ.name =  'ZZ'
WW.name = 'WW'
ll.name = 'll'
# ffbar.name = 'ffbar'

from fcc_ee_higgs.components.tools import load
load(comps)

from fcc_ee_higgs.plot.cuts import Cuts

cut_lepiso = '((sel_zeds_1_iso_e/sel_zeds_1_e<0.2) && (sel_zeds_2_iso_e/sel_zeds_2_e<0.2) && sel_zeds_1_e>0 && sel_zeds_2_e>0)'
cut_z_mass =  '(abs(sel_zeds_m-91)<15)'  # try opening this 
cut_z_kine = '(sel_zeds_pt>10 && sel_zeds_pz<50 && sel_zeds_acol>100 && sel_zeds_cross>10)'
cut_z_flavour = '(sel_zeds_1_pdgid==-sel_zeds_2_pdgid)'
cut_rad = '(((jets_1_e<0 || jets_1_22_e/jets_1_e<0.8) && \
(jets_2_e<0 || jets_2_22_e/jets_2_e<0.8)))'
cut_rad2 = '(jets_1_e>0 || (jets_1_e<0 && n_particles_not_zed==0))'
cut_htautau = '(((jets_1_211_num+jets_1_11_num+jets_1_13_num)==1 || (jets_1_211_num+jets_1_11_num+jets_1_13_num)==3) && \
 ((jets_2_211_num+jets_2_11_num+jets_2_13_num)==1 || (jets_2_211_num+jets_2_11_num+jets_2_13_num)==3))'
cut_htautau_or = '(((jets_1_211_num+jets_1_11_num+jets_1_13_num)==1 || (jets_1_211_num+jets_1_11_num+jets_1_13_num)==3) || \
 ((jets_2_211_num+jets_2_11_num+jets_2_13_num)==1 || (jets_2_211_num+jets_2_11_num+jets_2_13_num)==3))'
cut_htautau_1 = '((jets_1_211_num+jets_1_11_num+jets_1_13_num)==1 || (jets_1_211_num+jets_1_11_num+jets_1_13_num)==3)'
cut_missm = 'missing_energy_m/recoil_m<0.8'
cut_rm4l = '!((second_zeds_1_pdgid==-second_zeds_2_pdgid) && (abs(second_zeds_1_pdgid)==13 || abs(second_zeds_1_pdgid)==11))'
cut_leppt = '(sel_zeds_1_pt>10 && sel_zeds_2_pt>10)'
cut_hbb = get_cut_hbb(b_wp[0], b_wp[1], ' || ')
cut_not_hbb = '!({})'.format(cut_hbb)
cut_w_misse = '(missing_energy_e<70)'
cut_w_3body = 'abs(higgses_r_m - recoil_m)<15'

from fcc_ee_higgs.plot.cuts_gen import cut_gen_htautau

ZH.xSection *= 1.04

cuts = Cuts([
    # ('cut_gen_htautau', cut_gen_htautau), 
    ('cut_lepiso', cut_lepiso),
    ('cut_z_mass', cut_z_mass),
    ('cut_z_kine', cut_z_kine),
    ('cut_z_flavour', cut_z_flavour), 
    ('cut_rad2', cut_rad2), 
    # ('cut_rad', cut_rad),
    ('cut_htautau', cut_htautau), 
    # ('cut_htautau_or', cut_htautau_or),  
    # gain in precision! to investigate: try an or- nice but contamination is large of course...
    ('cut_rm4l', cut_rm4l),
    # ('cut_w_misse', cut_w_misse)
    ('cut_w_3body', cut_w_3body),
    ('cut_not_hbb', cut_not_hbb)
])

if var == 'sel_zeds_m':
    del cuts['cut_z_mass']
elif var == 'higgses_r_m - recoil_m':
    del cuts['cut_w_3body']
    bins = 50, -200, 200

cut = str(cuts)


