cut_gen_htautau = 'abs(genboson2_1_pdgid)==15'
cut_gen_hww = 'abs(genboson2_1_pdgid)==24'
cut_gen_hzz = 'abs(genboson2_1_pdgid)==23'
cut_gen_hbb = 'abs(genboson2_1_pdgid)==5'

from fcc_ee_higgs.plot.cuts import Cuts
cuts_gen = Cuts([
    ('cut_gen_htautau', cut_gen_htautau), 
    ('cut_gen_hbb', cut_gen_hbb), 
    ('cut_gen_hww', cut_gen_hww), 
    ('cut_gen_hzz', cut_gen_hzz), 
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
    if filename:
        with open(filename, 'w') as the_file:
            the_file.write('\n'.join(results))
