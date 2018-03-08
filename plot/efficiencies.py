import copy
import sys
from heppy.statistics.counter import Counter

class Efficiencies(object):
    
    #----------------------------------------------------------------------
    def __init__(self, tree, cuts):
        """"""
        self.cuts = cuts
        self.tree = tree

    def fill_cut_flow(self, cutflowname='Cuts', nevts=sys.maxint):
        self.cut_flow = Counter(cutflowname)
        ntot = min(self.tree.GetEntries(), nevts)
        nlast = ntot
        cut = '1'
        self.cut_flow.register('Preselection')
        self.cut_flow.inc('Preselection', ntot)
        for cutname, cutstr in self.cuts.iteritems():
            cut = ' && '.join([cut, cutstr])
            nsel = self.tree.GetEntries(cut)
            self.cut_flow.register(cutstr)
            self.cut_flow.inc(cutstr, nsel)
            nlast = nsel
        print self.cut_flow
        
    def marginal(self):
        all_cuts =  ' && '.join(self.cuts.values())
        print 'all cuts', all_cuts
        len_cutstr = max(len(cutstr) for cutstr in self.cuts.values()) + 5
        form = '{{cutstr:<{len_cutstr}}}\t{{eff:5.2f}}'.format(len_cutstr=len_cutstr)
        self.tree.Draw("1", all_cuts, "goff")
        nall = self.tree.GetSelectedRows()
        if not nall:
            print 'cannot compute marginal efficiencies, no events after full selection'
            return
        for cutname, cutstr in self.cuts.iteritems():
            # print cutname, cutstr
            cuts_nm1 = copy.copy(self.cuts)
            del cuts_nm1[cutname]
            the_cut = ' && '.join(cuts_nm1.values())
            # print the_cut
            self.tree.Draw("1", the_cut, "goff")
            nmarg = self.tree.GetSelectedRows()
            # print nmarg
            eff = '-1.0'
            if nmarg:
                eff = float(nall) / nmarg
            print form.format(cutstr=cutstr, eff=eff)
        
            
