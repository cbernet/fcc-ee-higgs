import heppy.framework.config as cfg
import heppy.utils.absglob as absglob
import compfiles

basedir = '/Users/cbernet/Code/FCC/fcc_ee_higgs/samples/pythia'

# definition of input samples 
ZH = cfg.MCComponent(
    'ZH',
    files = compfiles.get('{}/ZH'.format(basedir)),
    xSection = 0.00653, # pb-1
    nGenEvents = 4e4)

ZZ = cfg.MCComponent(
    'ZZ',
    files = compfiles.get('{}/ZZ'.format(basedir)),
    xSection = 1.360, # pb-1
    nGenEvents = 4e4)

WW = cfg.MCComponent(
    'WW',
    files = compfiles.get('{}/WW'.format(basedir)),
    # files = compfiles.get ('WW/Job_*/ee_WW.root'),
    xSection = 16.330, # pb-1
    nGenEvents = 4e4)

components = dict(
        ( (comp.name, comp) for comp in [ZH, ZZ, WW] )
)

if __name__ == '__main__':
    
    for comp in components.values():
        print comp
        
