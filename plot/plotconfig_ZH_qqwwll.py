var = 'higgs_r_m'
# var = 'higgs_r_m'

xtitle = 'm_{H} (GeV)'

channel = 'ww'

detector = 'CLD'
lumi = 5000e12

bins = 14, 80, 150

from fcc_ee_higgs.components.ZH_qqwwll_CLD_Jun7 import ZH, ZZ, ll, WW
comps = [ZZ, ZH, ll, WW]
ZH.name =  'ZH'
ZZ.name =  'ZZ'
WW.name = 'WW'
ll.name = 'll'

from fcc_ee_higgs.components.tools import load
load(comps)

from fcc_ee_higgs.plot.cuts import Cuts

##cut_lepiso = '((sel_zeds_1_iso_e/sel_zeds_1_e<0.4) && (sel_zeds_2_iso_e/sel_zeds_2_e<0.4) && sel_zeds_1_e>0 && sel_zeds_2_e>0)'
##cut_z_mass =  '(abs(sel_zeds_m-91)<15)'  # try opening this 
### cut_z_kine = '(sel_zeds_pt>10 && sel_zeds_pz<50 && sel_zeds_acol>100 && sel_zeds_cross>10)'
##cut_z_kine = 'sel_zeds_acol>110'
##cut_z_flavour = '(sel_zeds_1_pdgid==-sel_zeds_2_pdgid)'
####cut_rad = '(((jets_1_e<0 || jets_1_22_e/jets_1_e<0.8) && \
####(jets_2_e<0 || jets_2_22_e/jets_2_e<0.8)))'
####cut_rad2 = '(jets_1_e>0 || (jets_1_e<0 && n_particles_not_zed==0))'
####cut_rm4l = '!((second_zeds_1_pdgid==-second_zeds_2_pdgid) && (abs(second_zeds_1_pdgid)==13 || abs(second_zeds_1_pdgid)==11))'
##cut_hbb = get_cut_hbb(b_wp[0], b_wp[1], ' || ')
##
##cut_nophoton = '((jets_1_e<0 || jets_1_22_e/jets_1_e<0.95) && \
##(jets_2_e<0 || jets_2_22_e/jets_2_e<0.95) && \
##(jets_3_e<0 || jets_3_22_e/jets_3_e<0.95) && \
##(jets_4_e<0 || jets_4_22_e/jets_4_e<0.95))'
##
##alias_njets_nophoton = '(jets_1_e>0 && jets_1_22_e/jets_1_e<0.95) + \
##(jets_2_e>0 && jets_2_22_e/jets_2_e<0.95) + \
##(jets_3_e>0 && jets_3_22_e/jets_3_e<0.95) + \
##(jets_4_e>0 && jets_4_22_e/jets_4_e<0.95)'
##
##for comp in comps:
##    comp.tree.SetAlias('njets_nophoton', alias_njets_nophoton)
##
##
### my cuts
##cut_hadr_njets = '(njets_nophoton>=3)'
##cut_hadr_nptcs = '(sumjet_notzed_211_num>=10)'
##cut_hadr_nolep = '(n_iso_leptons_not_zed==0)'
##cut_not_hbb = '!({})'.format(cut_hbb)
##
### lep3 cuts
##cut_hadr_njets_lep3 = '(njets_nophoton>=4)'
##
##
##cut_lep_nleps = '(n_iso_leptons_not_zed>=1)'
##cut_lep_missinge = '(missing_energy_e>30)'
##cut_tau = '(n_jets==2 && missing_energy_e>50 && n_iso_leptons_not_zed==0)'
#### cut_hww = '({} || {} || {})'.format(cut_hadr, cut_lep, cut_tau)
####cut_w_3body = 'abs(higgses_r_m - recoil_m)<15'

cut_2leps = '(n_sel_iso_leptons>=2)'
cut_of = '(abs(sel_iso_leptons_1_pdgid)!=abs(sel_iso_leptons_2_pdgid))'
cut_os = '(sel_iso_leptons_1_q*sel_iso_leptons_2_q<0)'
cut_zedlep_m = '(zeds_lep_m>10 && zeds_lep_m<70)'
cut_zedlep_e = '(zeds_lep_e>80)'
cut_misse = '(missing_energy_e>40)'
cut_zedhad_m = '(abs(zeds_m-91)<10)'
cut_jetid = '(jets_1_211_num+jets_2_211_num>=10)'
cut_jetid_2 = '(jets_1_211_num>=4 && jets_2_211_num>=4 && (jets_1_211_num+jets_2_211_num>=10))'
cut_lepiso = '(sel_iso_leptons_1_iso_e/sel_iso_leptons_1_e<0.2 && \
sel_iso_leptons_2_iso_e/sel_iso_leptons_2_e<0.2 )'
cut_lepiso_comb = '((sel_iso_leptons_1_iso_e/sel_iso_leptons_1_e + \
sel_iso_leptons_2_iso_e/sel_iso_leptons_2_e)<0.4 )'
cut_tautau = '(abs(higgs_r_m-125)>15)'


from fcc_ee_higgs.plot.cuts_gen import * 

cuts = Cuts([
##    ('cut_gen', cut_gen_htautau), 
    ('cut_2leps', cut_2leps),
    ('cut_of', cut_of),
    ('cut_os', cut_os),
    ('cut_zedlep_m', cut_zedlep_m),
    # ('cut_zedlep_e', cut_zedlep_e),
    ('cut_misse', cut_misse),
    ('cut_zedhad_m', cut_zedhad_m),
    ('cut_jetid', cut_jetid_2),
    ('cut_lepiso', cut_lepiso_comb),
    ('cut_tautau', cut_tautau)
])

if var == 'zeds_m':
    del cuts['cut_zedhad_m']
    bins = 50, 0, 150    
if var == 'missing_energy_e':
    del cuts['cut_misse']
    bins = 50, 0, 150
if var == 'zeds_lep_m':
    del cuts['cut_zedlep_m']
    bins = 50, 0, 150
if var == 'zeds_lep_e':
    bins = 50, 0, 100
if var == 'higgs_r_m':
    del cuts['cut_tautau']
    
cut = str(cuts)


