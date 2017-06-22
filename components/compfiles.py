'''Find all rootfiles for a given sample.
'''

import os 
from heppy.utils import absglob as glob

def get(dirname):
    '''Returns the list of absolute paths for all root files in the sample.
     
    The sample must be on a standard filesystem,
    and the root files must be organized in the following way:
    
    dirname/*_*.root

    or:

    dirname/Job_*/*.root
    '''
    if not os.path.isdir(dirname):
        print '{} is not a directory'.format(dirname)
        return []
    rootfiles = glob.glob('{}/*_*.root'.format(dirname))
    if len(rootfiles):
        return rootfiles
    rootfiles = glob.glob('{}/Job*/*.root'.format(dirname)) 
    if len(rootfiles):
        return rootfiles
    print 'no rootfile found in component ' + dirname
    return []

if __name__ == '__main__':
    import sys
    import pprint
    pprint.pprint(get(sys.argv[1]))
    
