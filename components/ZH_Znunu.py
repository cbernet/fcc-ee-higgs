import os 
from fcc_datasets.fcc_component import FCCComponent
# import fcc_datasets.basedir as basedir
# basedir.basename = '/Users/cbernet/Datasets/FCC/fcc_ee_higgs/samples'

ZHnunu = FCCComponent(
    'heppy/ee_to_ZH_Z_to_nunu_H_to_bb/ee_to_ZZ_Oct23/pythia/ee_to_ZH_Z_to_nunu_Jun21_A_1',
    'fcc_ee_higgs.analyzers.ZHTreeProducer.ZHTreeProducer_1/tree.root', 
    xsection=132123,
    cache=False
)


components = dict(
        ( (comp.name, comp) for comp in [ZHnunu] )
)

if __name__ == '__main__':
    
    for comp in components.values():
        print comp
        
