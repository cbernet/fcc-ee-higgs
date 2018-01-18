import array
import sys

def add_csv(tree, csvmap, output_fname):
    nevents = tree.GetEntries()
    output_file = TFile(output_fname, 'recreate')
    newtree = tree.CloneTree(0)

    leaves = array.array("d", [-20., -20.])
    newbranch = newtree.Branch("csv", leaves, "jets_1_csv/D:jets_2_csv/D")

    print 'adding csv to ', nevents, 'events'
    for iev, event in enumerate(tree):
        if not (iev % 10000):
            print iev, event.jets_1_pt, event.jets_1_bmatch
        if iev == nevents:
            break
        iev += 1
        leaves[0] = csvmap.value(event.jets_1_pt, event.jets_1_bmatch)
        leaves[1] = csvmap.value(event.jets_2_pt, event.jets_2_bmatch)
        newtree.Fill()
    newtree.Write()
    output_file.Close()
            
if __name__ == '__main__':
    
    from ROOT import TFile
    from fcc_ee_higgs.plot.csv.csvmap import CSVMap
    
    if len(sys.argv) != 3:
        print 'usage: add_csv.py <tree.root> <csvmaps.root>'
        sys.exit(1)
        
    tree_fname, csvmaps_fname = sys.argv[1:]
    tree_rootfile = TFile(tree_fname)
    tree = tree_rootfile.Get('events')
    csvmap = CSVMap()
    csvmap.read(csvmaps_fname)
    
    add_csv(tree, csvmap, 'tree_with_csv.root')
