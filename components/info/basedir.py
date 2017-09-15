import os

def basedir(tier=None):
    base = '/afs/cern.ch/user/c/cbern/work/FCC/fcc_ee_higgs/samples'
    if os.getcwd().startswith('/Users'):
        base = '/Users/cbernet/Datasets/FCC/fcc_ee_higgs/samples'
    if tier is None:
        tier = ''
    elif tier not in ['pythia', 'heppy']:
        raise ValueError('tier must be set to pythia or heppy')
    base = '/'.join([base, tier])   
    if not os.path.isdir(base):
        raise ValueError('base sample directory {} does not exist'.format(base))
    return base

