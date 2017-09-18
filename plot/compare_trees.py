
from fcc_ee_higgs.components.all import components
from varmap_janik import varmap

cps = dict(
    janik=components['ee_to_ZZ_Janik_Sep18_ZHnunubb_A_10'],
    colin=components['ee_to_ZZ_Sep12_ZHnunubb_1b_A_5']
    )

for vcolin, vjanik in varmap.iteritems():
    cps['janik'].tree.SetAlias(vcolin, vjanik)
    
    
