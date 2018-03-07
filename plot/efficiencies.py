import copy

class Efficiencies(object):
    
    #----------------------------------------------------------------------
    def __init__(self, tree, cuts):
        """"""
        self.cuts = cuts
        self.tree = tree
        print self.cuts
        
    def marginal(self):
        all_cuts =  ' && '.join(self.cuts.values())
        print 'all cuts', all_cuts
        nall = self.tree.Draw("1", all_cuts, "goff")
        print 'nsel', nall
        for cutname, cutstr in self.cuts.iteritems():
            print cutname, cutstr
            cuts_nm1 = copy.copy(self.cuts)
            del cuts_nm1[cutname]
            the_cut = ' && '.join(cuts_nm1.values())
            print the_cut
            self.tree.Draw("1", the_cut, "goff")
            nmarg = self.tree.GetSelectedRows()
            print nmarg
            print 'marginal eff', float(nall) / nmarg
        
            
