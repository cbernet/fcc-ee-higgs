import copy
import sys
from heppy.statistics.counter import Counter

class Efficiencies(object):
    
    #----------------------------------------------------------------------
    def __init__(self, tree, cuts):
        """"""
        self.cuts = cuts
        self.tree = tree
        self.cut_flow = None

    def fill_cut_flow(self, cutflowname='Cuts', nevts=sys.maxint):
        self.cut_flow = Counter(cutflowname)
        ntot = min(self.tree.GetEntries(), nevts)
        nlast = ntot
        cut = '1'
        self.cut_flow.register('Preselection')
        self.cut_flow.inc('Preselection', ntot)
        for cutname, cutstr in self.cuts.iteritems():
            cut = ' && '.join([cut, cutstr])
            self.tree.Draw('1', cut, 'goff', nevts)
            nsel = self.tree.GetSelectedRows()
            self.cut_flow.register(cutname)
            self.cut_flow.inc(cutname, nsel)
            nlast = nsel
    
    def str_cut_flow(self):
        the_str = []
        for cutname, cutstr in self.cuts.iteritems():
            the_str.append('{:<20} {}'.format(cutname, cutstr))
        the_str.append(str(self.cut_flow))
        return '\n'.join(the_str)
        
    def write(self, fname):
        the_file = open(fname, 'w')
        the_file.write(self.str_cut_flow())
        the_file.close()
        
    def marginal(self):
        all_cuts =  ' && '.join(self.cuts.values())
        print 'all cuts', all_cuts
        len_cutname = max(len(cutname) for cutname in self.cuts) + 5
        form = '{{cutname:<{len_cutname}}}\t{{eff:5.2f}}'.format(len_cutname=len_cutname)
        self.tree.Draw("1", all_cuts, "goff")
        nall = self.tree.GetSelectedRows()
        if not nall:
            print 'cannot compute marginal efficiencies, no events after full selection'
            return
        for cutname, cutstr in self.cuts.iteritems():
            # print cutname, cutstr
            the_cut = self.cuts.marginal(cutname).__str__()
            # print the_cut
            self.tree.Draw("1", the_cut, "goff")
            nmarg = self.tree.GetSelectedRows()
            # print nmarg
            eff = '-1.0'
            if nmarg:
                eff = float(nall) / nmarg
            print form.format(cutname=cutname, eff=eff)


