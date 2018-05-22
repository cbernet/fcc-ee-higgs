import pprint 

# higgs

cut_gen_htautau = 'abs(genboson2_1_pdgid)==15'
cut_gen_hww = 'abs(genboson2_1_pdgid)==24'
cut_gen_hzz = 'abs(genboson2_1_pdgid)==23'
cut_gen_hbb = 'abs(genboson2_1_pdgid)==5'
cut_gen_hcc = 'abs(genboson2_1_pdgid)==4'
cut_gen_hgg = 'abs(genboson2_1_pdgid)==21'

from fcc_ee_higgs.plot.cuts import Cuts
cuts_gen = Cuts([
    ('cut_gen_htautau', cut_gen_htautau), 
    ('cut_gen_hww', cut_gen_hww), 
    ('cut_gen_hzz', cut_gen_hzz), 
    ('cut_gen_hbb', cut_gen_hbb), 
    ('cut_gen_hcc', cut_gen_hcc),
    ('cut_gen_hgg', cut_gen_hgg), 
    
])

def signal_contamination(tree, cut, filename=None):
    nsel = float(tree.GetEntries(cut))
    the_file = None
    results = []
    for cutname, dmode in cuts_gen.iteritems():
        nseldmode = tree.GetEntries('&&'.join([cut, dmode]) )
        contamination = nseldmode / nsel * 100.
        the_str = '{} : {} %'.format(cutname, contamination)
        results.append(the_str)
        print the_str
    if filename:
        with open(filename, 'w') as the_file:
            the_file.write('\n'.join(results))

# W

cut_gen_w1_lep = '(abs(genw1_1_pdgid)==11 || abs(genw1_1_pdgid)==13)'
cut_gen_w2_lep = '(abs(genw2_1_pdgid)==11 || abs(genw2_1_pdgid)==13)'
cut_gen_ww_2lep = '({} && {})'.format(cut_gen_w1_lep, cut_gen_w2_lep)
cut_gen_ww_1lep = '(({} || {}) && !{})'.format(cut_gen_w1_lep, cut_gen_w2_lep,
                                             cut_gen_ww_2lep)
cut_gen_w1_tau = '(abs(genw1_1_pdgid)==15)'
cut_gen_w2_tau = '(abs(genw2_1_pdgid)==15)'
cut_gen_ww_1tau = '(({} || {}) && !{} && !{})'.format(
    cut_gen_w1_tau, cut_gen_w2_tau, cut_gen_ww_1lep, cut_gen_ww_2lep
)
cut_gen_w1_had = '(abs(genw1_1_pdgid)<5)'
cut_gen_w2_had = '(abs(genw2_1_pdgid)<5)'
cut_gen_ww_had = '({} && {})'.format(cut_gen_w1_had, cut_gen_w2_had)

cut_gen_ww_other = '(!{} && !{} && !{} && !{})'.format(
    cut_gen_ww_2lep, cut_gen_ww_1lep, cut_gen_ww_1tau, cut_gen_ww_had
)

cuts_gen_ww = Cuts([
    ('cut_gen_ww_2lep', cut_gen_ww_2lep), 
    ('cut_gen_ww_1lep', cut_gen_ww_1lep), 
    ('cut_gen_ww_1tau', cut_gen_ww_1tau), 
    ('cut_gen_ww_had', cut_gen_ww_had), 
])
