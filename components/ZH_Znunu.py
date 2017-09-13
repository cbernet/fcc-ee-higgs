import os 
import heppy.framework.config as cfg
import heppy.utils.absglob as absglob
import compfiles

   
# basedir = '/afs/cern.ch/user/c/cbern/FCC/fcc_ee_higgs/pythia'
basedir = '/afs/cern.ch/user/c/cbern/work/FCC/fcc_ee_higgs/pythia'

if os.getcwd().startswith('/Users'):
    basedir = '/Users/cbernet/Code/FCC/fcc_ee_higgs/samples/analysis'

# definition of input samples 
ZHnunu = cfg.MCComponent(
    'ZHnunu',
    files = compfiles.get('{}/ZHnunu/June21'.format(basedir)),
    xSection = 0.013, # pb-1
    nGenEvents = 100*5000)

ZZnunu = cfg.MCComponent(
    'ZZnunu',
    files = compfiles.get('{}/ZZnunu/June21'.format(basedir)),
    xSection = 1.360, # pb-1
    nGenEvents = 200*5000*34870/5000.)

ZZ = cfg.MCComponent(
    'ZZ',
    files = compfiles.get('{}/ZZ/Sep12_2M'.format(basedir)),
    xSection = 1.360, # pb-1
    nGenEvents = 200*5000*34870/5000.)

WW = cfg.MCComponent(
    'WW',
    # files = compfiles.get('{}/WWnunu/June21'.format(basedir)),
    # files = compfiles.get ('WW/Job_*/ee_WW.root'),
    files = [],
    xSection = 16.330, # pb-1
    nGenEvents = 8.5e6)

components = dict(
        ( (comp.name, comp) for comp in [ZHnunu, ZZ] )
)

if __name__ == '__main__':
    
    for comp in components.values():
        print comp
        
