import os 
import heppy.framework.config as cfg
import heppy.utils.absglob as absglob
import compfiles

   
# basedir = '/afs/cern.ch/user/c/cbern/FCC/fcc_ee_higgs/pythia'
basedir = '/afs/cern.ch/user/c/cbern/work/FCC/fcc_ee_higgs/pythia'

if os.getcwd().startswith('/Users'):
    basedir = '/Users/cbernet/Code/FCC/fcc_ee_higgs/samples/pythia'

# definition of input samples 
ZH = cfg.MCComponent(
    'ZH',
    files = compfiles.get('{}/ZH'.format(basedir)),
    xSection = 2e-1, # pb-1
    nGenEvents = 840e3)

ZZ = cfg.MCComponent(
    'ZZ',
    files = compfiles.get('{}/ZZ'.format(basedir)),
    xSection = 1.360, # pb-1
    nGenEvents = 2.05e6)

WW = cfg.MCComponent(
    'WW',
    files = compfiles.get('{}/WW'.format(basedir)),
    # files = compfiles.get ('WW/Job_*/ee_WW.root'),
    xSection = 16.330, # pb-1
    nGenEvents = 8.5e6)

components = dict(
        ( (comp.name, comp) for comp in [ZH, ZZ, WW] )
)

if __name__ == '__main__':
    
    for comp in components.values():
        print comp
        
