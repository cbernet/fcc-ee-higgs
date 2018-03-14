from collections import OrderedDict

class Cuts(OrderedDict):

    def __init__(self, items):
        super(Cuts, self).__init__(items)
        
    def print_cuts(self):
        for key, value in self.iteritems():
            print key, value
    
    def __str__(self):
        return ' && '.join(self.values())
   
