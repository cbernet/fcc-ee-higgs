from heppy.framework.config import MCComponent

import os 
import glob
import yaml
import pprint

########################################################################
class FCCComponent(MCComponent):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, sample_fname):
        """Constructor"""
        if not os.path.isdir(sample_fname):
            raise ValueError('directory {} does not exist'.format(sample_fname))
        info_fnames = glob.glob(sample_fname+'/*.yaml')
        if len(info_fnames) > 1:
            raise ValueError('more than one yaml file in '+sample_fname)
        elif len(info_fnames) == 0:
            raise ValueError('no yaml file in '+sample_fname)                    
        tmp = open(info_fnames[0])
        self.info = yaml.load(tmp)['sample']
        # get n gen events and cross section from mother
        
            
    def __str__(self):
        return pprint.pformat(self.info)
    

            
    
    
