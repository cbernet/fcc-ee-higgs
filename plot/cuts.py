from collections import OrderedDict

class Cuts(OrderedDict):

    def __init__(self, items):
        super(Cuts, self).__init__(items)
    
    def __str__(self):
        return ' && '.join(self.values())
   
