var = 'higgses_rescaled_0_m'
# var = 'higgs_r_m'

xtitle = 'm_{H} (GeV)'

channel = 'nunuww'

detector = 'CLD'
lumi = 5000e12

bins = 30, 80, 140

from fcc_ee_higgs.components.ZH_nunuww_CLD_jun13_B import ZH, ZZ, WW, ffbar
comps = [ZZ, ZH, WW, ffbar]
ZH.name =  'ZH'
ZZ.name =  'ZZ'
WW.name = 'WW'
ffbar.name = 'ffbar'
ffbar.smooth = 1
WW.smooth = 1
ZZ.smooth = 1

from fcc_ee_higgs.components.tools import load
load(comps)

from fcc_ee_higgs.plot.cuts import Cuts

from fcc_ee_higgs.plot.cuts_gen_2 import * 

cut_missmass = '(missing_energy_0_m>80)'
cut_misse = '(missing_energy_0_e>80)'
cut_theta = '(abs(missing_energy_0_theta*180/3.14) < 65)'
cut_mwstar = '(wstar_0_m>10)'
cut_jete = '(jets4_2_e)>15'

def get_cut_hbb(eff, fake, jets, n, operator=' && '):
    strings = []
    for i in range(n):
        string = '(({jets}_{i}_bmatch==1 && rndm<{eff}) || ({jets}_{i}_bmatch==0 && rndm<{fake}))'.format(
            jets=jets, i=i, eff=eff, fake=fake
        )
        strings.append(string)
    return operator.join(strings)
        
eff, fake = (0.8, 4e-3)

cut_hbb = get_cut_hbb(eff, fake, 'jets4', 4, ' || ')
cut_not_hbb = '!({})'.format(cut_hbb)
cut_higgs_acol = '(higgses_0_acol>100)'

cut_notau = '!(\
(sel_iso_taus_0_e>0 && sel_iso_taus_0_iso_e/sel_iso_taus_0_e<0.2) || \
(sel_iso_taus_1_e>0 && sel_iso_taus_1_iso_e/sel_iso_taus_1_e<0.2) || \
(sel_iso_taus_2_e>0 && sel_iso_taus_2_iso_e/sel_iso_taus_2_e<0.2) || \
(sel_iso_taus_3_e>0 && sel_iso_taus_3_iso_e/sel_iso_taus_3_e<0.2) \
)'

def get_cut_notau():
    strings = []
    for i in range(4):
        strings.append('(n_sel_iso_taus<={i} || sel_iso_taus_{i}_iso_e/sel_iso_taus_{i}_e<0.2)'.format(i=i))
    return ' && '.join(strings)
##cut_notau = get_cut_notau()

cuts = Cuts([
    ('cut_missmass', cut_missmass),
    # ('cut_misse', cut_misse),
    ('cut_theta', cut_theta),
    ('cut_mwstar', cut_mwstar),
    ('cut_jete', cut_jete),
    ('cut_not_hbb', cut_not_hbb),
    ('cut_higgs_acol', cut_higgs_acol),
    ('cut_notau', cut_notau)
])

cut = str(cuts)

# cut = ''

