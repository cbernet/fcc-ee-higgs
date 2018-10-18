import array
import sys
import os

from ROOT import TMVA, TString, TFile

def init_reader(method, weights_fname, variables):
    reader = TMVA.Reader()    
    arrays = dict()
    arrays_d = dict()
    for variable in variables:
        arr = array.array('f', [0.0])
        arrays[variable] = arr
        arrays_d[variable] = array.array('d', [0.0])
        reader.AddVariable(variable, arr)
    reader.BookMVA(method, weights_fname)
    return reader, arrays, arrays_d


def add_mva(input_fname, weights_fname):
    tree_rootfile = TFile(tree_fname)
    tree = tree_rootfile.Get('events')
    
    nevents = tree.GetEntries()
    tree.SetBranchStatus('mva', 0)
    
    output_fname = 'tree_with_mva.root'    
    output_file = TFile(output_fname, 'recreate')
    
    newtree = tree.CloneTree(0)
    
    leaves = array.array("d", [-20.])
    newbranch = newtree.Branch("mva", leaves, "mva/D")

    method = 'BDTG'
    variables = ['zeds_m',
                 'zeds_theta',
                 'zeds_1_theta', 'zeds_2_theta',
                 'zeds_acol',
                 # 'zeds_cross', 'zeds_pz'
                 ]
    reader, arrays, arrays_d = init_reader(method, weights_fname,
                                           variables)
    for variable in variables: 
        tree.SetBranchAddress( variable, arrays_d[variable] )
    
    print 'adding mva to ', nevents, 'events'
    for iev in range(min(tree.GetEntries(), nevents)):
        if not (iev % 10000):
            print iev
        if iev == nevents:
            break
        tree.GetEntry(iev)
        for var in variables:
            arrays[var][0] = arrays_d[var][0]
        mva = reader.EvaluateMVA( method )
        leaves[0] = mva
        newtree.Fill()
    newtree.Write()
    output_file.Close()

    directory, basename = os.path.split(tree_fname)
    basename = 'old_' + basename
    backup_fname = '/'.join([directory, basename])
    shutil.move(tree_fname, backup_fname)
    shutil.move(output_fname, tree_fname)
    print 'your tree now contains mva values:'
    print tree_fname
    print 'original file copied to:'
    print backup_fname
            
if __name__ == '__main__':
    
    from ROOT import TFile
    import shutil
    
    if len(sys.argv) != 3:
        print 'usage: add_mva.py <tree.root> <mva_weights>'
        sys.exit(1)
        
    tree_fname, weights_fname = sys.argv[1:]
    add_mva(tree_fname, weights_fname)
