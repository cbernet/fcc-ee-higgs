import copy
from heppy.statistics.counter import Counter

class Efficiencies(object):
    
    #----------------------------------------------------------------------
    def __init__(self, tree, cuts):
        """"""
        self.cuts = cuts
        self.tree = tree

    def fill_cut_flow(self):
        self.cut_flow = Counter('Cuts')
        ntot = self.tree.GetEntries()
        nlast = ntot
        cut = '1'
        self.cut_flow.register('Preselection')
        self.cut_flow.inc('Preselection', ntot)
        for cutname, cutstr in self.cuts.iteritems():
            cut = ' && '.join([cut, cutstr])
            print cutstr
            self.tree.Draw("1", cut, 'goff')
            nsel = self.tree.GetSelectedRows()
            self.cut_flow.register(cutstr)
            self.cut_flow.inc(cutstr, nsel)
            print nsel, float(nsel) / ntot, float(nsel) / nlast
            nlast = nsel
        print self.cut_flow
        
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
        
            
