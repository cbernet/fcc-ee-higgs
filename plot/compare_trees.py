
from fcc_ee_higgs.components.all import load_components
all_components = load_components()

from varmap_janik import varmap
from cpyroot.tools.treecomparator import TreeComparator
from cpyroot.tools.splitcanvas import SplitCanvas
from ROOT import TPad, TCanvas

import pprint 

def print_vars(tree):
    names = []
    for v in tree.GetListOfBranches():
        names.append(v.GetName())
    pprint.pprint(names)

comps = dict(
    janik=all_components['ee_to_ZZ_Janik_Sep18_ZHnunubb_A_10'],
    colin=all_components['ee_to_ZZ_Sep19_ZHnunubb_A_11']
    )

for vcolin, vjanik in varmap.iteritems():
    comps['janik'].tree.SetAlias(vcolin, vjanik)
    
tc = comps['colin'].tree
tj = comps['janik'].tree

vars = [
    'higgs_acol',
    'higgs_cross', 
    'higgs_rescaled_m',
    'higgs_rescaled_pt',
    'jet1_e',
    'jet2_e',
    'jet1_b',
    'misenergy_m',
    'misenergy_pz',
    'misenergy_pt',
    
]

args = {
    'jet1_b': dict(nbins = 2, xmin = 0, xmax = 2),
}

cut = 'jet1_e>0 && jet2_e>0'

canvas = SplitCanvas(len(vars), 'canvas', 'title', 400)

cp = TreeComparator(tc, tj, 'colin', 'janik', normalize=-1)

for ivar, var in enumerate(vars):
    canvas.cd(ivar+1)
    print TPad.Pad()
    kwargs = args.get(var, dict())
    cp.draw(var, cut=cut, **kwargs)
