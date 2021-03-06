var = 'recoil_m'
# var = 'missing_energy_e'

xtitle = 'm_{H} (GeV)'

channel = 'ww_1lep'

detector = 'CLD'
lumi = 5000e12

bins = 50, 50, 150

def get_cut_hbb(eff, fake, operator='||'):
    return '( \
((jets_1_bmatch==1 && rndm<{eff}) || (jets_1_bmatch==0 && rndm<{fake})) || \
((jets_2_bmatch==1 && rndm<{eff}) || (jets_2_bmatch==0 && rndm<{fake})) || \
((jets_3_bmatch==1 && rndm<{eff}) || (jets_3_bmatch==0 && rndm<{fake})) || \
((jets_4_bmatch==1 && rndm<{eff}) || (jets_4_bmatch==0 && rndm<{fake})))'.format(eff=eff, fake=fake, op=operator)

b_wp = (0.8, 4e-3)

from fcc_ee_higgs.components.ZH_llww_CLD_May23 import ZH, ZZ, ll, WW
comps = [ZZ, ZH, ll, WW]
ZH.name =  'ZH'
ZZ.name =  'ZZ'
WW.name = 'WW'
ll.name = 'll'
ZZ.smooth = True

from fcc_ee_higgs.components.tools import load
load(comps)

from fcc_ee_higgs.plot.cuts import Cuts

cut_lepiso = '((sel_zeds_1_iso_e/sel_zeds_1_e<0.4) && (sel_zeds_2_iso_e/sel_zeds_2_e<0.4) && sel_zeds_1_e>0 && sel_zeds_2_e>0)'
cut_z_mass =  '(abs(sel_zeds_m-91)<15)'  # try opening this 
# cut_z_kine = '(sel_zeds_pt>10 && sel_zeds_pz<50 && sel_zeds_acol>100 && sel_zeds_cross>10)'
cut_z_kine = 'sel_zeds_acol>110'
cut_z_flavour = '(sel_zeds_1_pdgid==-sel_zeds_2_pdgid)'
##cut_rad = '(((jets_1_e<0 || jets_1_22_e/jets_1_e<0.8) && \
##(jets_2_e<0 || jets_2_22_e/jets_2_e<0.8)))'
##cut_rad2 = '(jets_1_e>0 || (jets_1_e<0 && n_particles_not_zed==0))'
##cut_rm4l = '!((second_zeds_1_pdgid==-second_zeds_2_pdgid) && (abs(second_zeds_1_pdgid)==13 || abs(second_zeds_1_pdgid)==11))'
cut_hbb = get_cut_hbb(b_wp[0], b_wp[1], ' || ')

##cut_nophoton = '((jets_1_e<0 || jets_1_22_e/jets_1_e<0.95) && \
##(jets_2_e<0 || jets_2_22_e/jets_2_e<0.95) && \
##(jets_3_e<0 || jets_3_22_e/jets_3_e<0.95) && \
##(jets_4_e<0 || jets_4_22_e/jets_4_e<0.95))'

##alias_njets_nophoton = '(jets_1_e>5 && jets_1_22_e/jets_1_e<0.95) + \
##(jets_2_e>5 && jets_2_22_e/jets_2_e<0.95) + \
##(jets_3_e>5 && jets_3_22_e/jets_3_e<0.95) + \
##(jets_4_e>5 && jets_4_22_e/jets_4_e<0.95)'

emin = 5

cut_nophoton = '((jets_1_e<{emin} || jets_1_22_e/jets_1_e<0.95) && \
(jets_2_e<{emin} || jets_2_22_e/jets_2_e<0.95) && \
(jets_3_e<{emin} || jets_3_22_e/jets_3_e<0.95) && \
(jets_4_e<{emin} || jets_4_22_e/jets_4_e<0.95))'.format(emin=emin)

alias_njets_nophoton = '(jets_1_e>{emin} && jets_1_22_e/jets_1_e<0.95) + \
(jets_2_e>{emin} && jets_2_22_e/jets_2_e<0.95) + \
(jets_3_e>{emin} && jets_3_22_e/jets_3_e<0.95) + \
(jets_4_e>{emin} && jets_4_22_e/jets_4_e<0.95)'.format(emin=emin)

for comp in comps:
    comp.tree.SetAlias('njets_nophoton', alias_njets_nophoton)

cut_lep_nleps = '(n_iso_leptons_not_zed>=1)'
cut_not_hbb = '!({})'.format(cut_hbb)
cut_lep_njets = '(njets_nophoton>=2)'
# cut_lep_missinge = '(missing_energy_e>15)'
cut_lep_nptcsnotzed = '(n_particles_not_zed>7)'

##cut_nophoton = '((jets_1_e<0 || jets_1_22_e/jets_1_e<0.95) && \
##(jets_2_e<0 || jets_2_22_e/jets_2_e<0.95) && \
##(jets_3_e<0 || jets_3_22_e/jets_3_e<0.95) && \
##(jets_4_e<0 || jets_4_22_e/jets_4_e<0.95))'
from fcc_ee_higgs.plot.cuts_gen import * 

cuts_lep = Cuts([
    # ('cut_gen_ww_had', cut_gen_ww_had), 
    ('cut_lepiso', cut_lepiso),
    ('cut_z_mass', cut_z_mass),
    ('cut_z_kine', cut_z_kine),
    ('cut_z_flavour', cut_z_flavour),
    ('cut_lep_nleps', cut_lep_nleps),
    ('cut_lep_njets', cut_lep_njets),
    # ('cut_lep_missinge', cut_lep_missinge),
    # ('cut_nophoton', cut_nophoton), 
    ('cut_lep_nptcsnotzed', cut_lep_nptcsnotzed), 
    ('cut_not_hbb', cut_not_hbb),
##    ('cut_nophoton', cut_nophoton)
])

cuts = cuts_lep

if var == 'sel_zeds_m':
    del cuts['cut_z_mass']
elif var == 'missing_energy_e':
    bins = (50, 0, 100)
    del cuts['cut_lep_missinge']
cut = str(cuts)


