import heppy.framework.config as cfg
import heppy.utils.absglob as absglob

basedir = '/Users/cbernet/Code/FCC/fcc-ee-higgs/samples/pythia'

# definition of input samples 
ZH_Zmumu = cfg.MCComponent(
    'ZH_Zmumu',
    files = absglob.glob('{}/mumu/ZH/ee_ZH_Zmumu_*.root'.format(basedir)),
    xSection = 0.00653, # pb-1
    nGenEvents = 4e4)

ZZ = cfg.MCComponent(
    'ZZ',
    files = absglob.glob('{}/ZZ/ee_ZZ_*.root'.format(basedir)),
    xSection = 1.360, # pb-1
    nGenEvents = 4e4)

WW = cfg.MCComponent(
    'WW',
    files = absglob.glob('{}/WW/ee_WW_*.root'.format(basedir)),
    # files = absglob.glob('WW/Job_*/ee_WW.root'),
    xSection = 16.330, # pb-1
    nGenEvents = 4e4)

components = dict(
        ( (comp.name, comp) for comp in [ZH_Zmumu, ZZ, WW] )
)

if __name__ == '__main__':
    
    for comp in components.values():
        print comp
        
