

def marginal_efficiency(tree, cuts):
    tree.Draw('1', ' && '.join(cuts))
    num = float(tree.GetSelectedRows())
    print cuts
    efficiencies = dict()
    for cut in cuts:
        other_cuts = list(cuts)
        other_cuts.remove(cut)
        print other_cuts
        str_other_cuts = ' && '.join(other_cuts)
        tree.Draw('1', str_other_cuts, 'goff')
        denom = float(tree.GetSelectedRows())
        eff = num / denom
        efficiencies[cut] = eff
    return efficiencies

def print_table(efficiencies):
    for cut, eff in efficiencies.iteritems():
        print '{cut:>40}\t{eff:5.2f}'.format(cut=cut, eff=eff)
