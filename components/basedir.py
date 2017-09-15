import os

def basedir(tier):
    if tier not in ['pythia', 'heppy']:
        raise ValueError('tier must be set to pythia or heppy')
    base = '/afs/cern.ch/user/c/cbern/work/FCC/fcc_ee_higgs/samples/{}'.format(tier)  #TODO update 
    if os.getcwd().startswith('/Users'):
        base = '/Users/cbernet/Datasets/FCC/fcc_ee_higgs/samples/{}'.format(tier)
    if not os.path.isdir(base):
        raise ValueError('base sample directory {} does not exist'.format(base))
    return base
