import itertools
import array

from heppy.utils.deltar import deltaR
import heppy
heppy.configuration.Collider.BEAMS == 'ee'

def drmin(event):
    drmin = 999999.
    for i, j in itertools.combinations(range(4), 2):
        theta1 = getattr(event, 'jets4_{}_theta'.format(i))
        phi1 = getattr(event, 'jets4_{}_phi'.format(i))
        theta2 = getattr(event, 'jets4_{}_theta'.format(j))
        phi2 = getattr(event, 'jets4_{}_phi'.format(j))
        dr = deltaR(theta1, phi1, theta2, phi2)
        if dr < drmin:
            drmin = dr
    return drmin

def add_drmin(tree, output_fname):
    maxevents = sys.maxint
    nevents = min(maxevents, tree.GetEntries())
    output_file = TFile(output_fname, 'recreate')
    newtree = tree.CloneTree(0)

    leaves = array.array("d", [-99])
    newbranch = newtree.Branch("drmin", leaves, "drmin/D")

    print 'adding drmin to ', nevents, 'events'
    for iev, event in enumerate(tree):
        if not (iev % 10000):
            print iev
        if iev == nevents:
            break
        iev += 1
        leaves[0] = drmin(event)
        newtree.Fill()
    newtree.Write()
    output_file.Close()    
    
if __name__ == '__main__':
    
    from ROOT import TFile
    import shutil
    import sys
    
    if len(sys.argv) != 2:
        print 'usage: add_csv.py <tree.root>'
        sys.exit(1)
        
    tree_fname = sys.argv[1]
    tree_rootfile = TFile(tree_fname)
    tree = tree_rootfile.Get('events')

    treedrmin_fname = 'tree_with_drmin.root'
    add_drmin(tree, treedrmin_fname)
##    backup_fname = 'old_'+tree_fname
##    shutil.move(tree_fname, backup_fname)
##    shutil.move(treedrmin_fname, tree_fname)
##    print 'your tree now contains drmin values.'
##    print 'original file copied to', backup_fname
