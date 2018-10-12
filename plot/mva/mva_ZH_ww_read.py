from ROOT import TMVA, TString, TFile
import array
import sys

from fcc_ee_higgs.plot.plotconfig_ilc_ZH_ll import ZH, WW

method = "BDTG"

variables = ['zeds_m',
             'zeds_theta',
             'zeds_1_theta', 'zeds_2_theta',
             'zeds_acol', 'zeds_cross', 'zeds_pz']

reader = TMVA.Reader()

arrays = dict()
arrays_d = dict()
for variable in variables:
    arr = array.array('f', [0.0])
    arrays[variable] = arr
    arrays_d[variable] = array.array('d', [0.0])
    reader.AddVariable(variable, arr)
    
reader.BookMVA(method, "dataset/weights/TMVAClassification_BDTG.weights.xml")

output_fname = 'ZH.root'
tree = ZH.tree
verbose = False

for variable in variables: 
    tree.SetBranchAddress( variable, arrays_d[variable] )

nevents = sys.maxint
output_file = TFile(output_fname, 'recreate')
newtree = tree.CloneTree(0)

leaves = array.array("d", [-20.])
newbranch = newtree.Branch("mva", leaves, "mva/D")

for i in range(min(tree.GetEntries(), nevents)):
    if (i % 1000) == 0:
        print i 
    tree.GetEntry(i)
    if verbose:
        print '-' * 70
    for var in variables:
        if verbose:
            print getattr(tree, var)
            print arrays_d[var][0]
        arrays[var][0] = arrays_d[var][0]
    mva = reader.EvaluateMVA( method )
    if verbose:
        print mva
    leaves[0] = mva
    newtree.Fill()
newtree.Write()
output_file.Close()
