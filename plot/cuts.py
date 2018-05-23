from collections import OrderedDict
import copy

class Cuts(OrderedDict):

    def __init__(self, items):
        super(Cuts, self).__init__(items)
        
    def print_cuts(self):
        for key, value in self.iteritems():
            print key, value
    
    def marginal(self, cutname):
        marg_cuts = copy.copy(self)
        del marg_cuts[cutname]
        return marg_cuts

    def __str__(self):
        return ' && '.join(self.values())
   
