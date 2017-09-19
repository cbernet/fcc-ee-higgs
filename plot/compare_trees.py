
from fcc_ee_higgs.components.all import components
from varmap_janik import varmap
from cpyroot.tools.treecomparator import TreeComparator

import pprint 

def print_vars(tree):
    names = []
    for v in tree.GetListOfBranches():
        names.append(v.GetName())
    pprint.pprint(names)

comps = dict(
    janik=components['ee_to_ZZ_Janik_Sep18_ZHnunubb_A_10'],
    colin=components['ee_to_ZZ_Sep12_ZHnunubb_A_9']
    )

for vcolin, vjanik in varmap.iteritems():
    comps['janik'].tree.SetAlias(vcolin, vjanik)
    
tc = comps['colin'].tree
tj = comps['janik'].tree

cp = TreeComparator(tc, tj, 'colin', 'janik', normalize=-1)

vars = [
    'higgs_acol',
    'higgs_cross', 
    'higgs_m',
    'jet1_e',
    'jet2_e', 
]

for var in vars:
    cp.draw(var)
