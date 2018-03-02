from ROOT import TH2F, TFile, TTree

class CSVMap(object):
    
    def __init__(self, histmap_b=None, histmap_other=None):
        # check that both are none or that both are defined
        self.histmap_b = histmap_b
        self.histmap_other = histmap_other
        self.histmaps1d_b = None
        self.histmaps1d_other = None
        if histmap_b and histmap_other:
            self.histmaps1d_b = self.build_1d_maps(histmap_b)
            self.histmaps1d_other = self.build_1d_maps(histmap_other)
        
        
    def pdf(self, pt, is_b):
        '''Get 1D map depending on pt and flavour'''
        histmaps1d = self.histmaps1d_b if is_b else self.histmaps1d_other
        ibin = self.pthist.FindBin(pt)
        if ibin == 0:
            return None  #underflow, pt too low
        else:
            return histmaps1d[ibin]
   
    def value(self, pt, is_b):
        pdf = self.pdf(pt, is_b)
        if pdf:
            return pdf.GetRandom()
        else:
            return -15
        
    def build_map(self, fname, *bindef):
        self.rootfile = TFile(fname)
        self.tree = self.rootfile.Get("JetTree")
        nentries = int(5e7)
        self.histmap_b = TH2F("csvmap_b", "csvmap_b", *bindef)
        self.histmap_other = self.histmap_b.Clone("csvmap_other")
        print 'building csv map for b jets..'
        self.tree.Project(self.histmap_b.GetName(),
                          "JetCSV:JetPt", "JetFlavour==5", "", 
                          nentries)
        print 'building csv map for other jets..'
        self.tree.Project(self.histmap_other.GetName(),
                          "JetCSV:JetPt", "JetFlavour!=5", "", 
                          nentries)
        print 'done.'
        # normalize each bin in pT
        self.histmap_b = normalize_map(self.histmap_b)
        self.histmap_other = normalize_map(self.histmap_other)
        self.histmaps1d_b = self.build_1d_maps(self.histmap_b)
        self.histmaps1d_other = self.build_1d_maps(self.histmap_other)
        self.write('csvmaps.root')
        
    def build_1d_maps(self, hist2d):
        dict1d = dict()
        for xbin in range(1, hist2d.GetNbinsX() + 1):
            projname = '{}_{}'.format(hist2d.GetName(), str(xbin))
            map1d = hist2d.ProjectionY(projname, xbin, xbin, "")
            print xbin, map1d
            dict1d[xbin] = map1d
        # dealing with overflow
        dict1d[xbin+1] = map1d
        self.pthist = hist2d.ProjectionX()
        return dict1d
            
    def write(self, fname):
        rootfile = TFile(fname, 'recreate')
        self.histmap_b.Write()
        self.histmap_other.Write()
        rootfile.Close()
    
    def read(self, fname):
        self.irootfile = TFile(fname)
        self.histmap_b = self.irootfile.Get('csvmap_b_norm')
        self.histmap_other = self.irootfile.Get('csvmap_other_norm')
        self.histmaps1d_b = self.build_1d_maps(self.histmap_b)
        self.histmaps1d_other = self.build_1d_maps(self.histmap_other)
        
            
def normalize_map(hist):
    hist_norm = hist.Clone(hist.GetName() + '_norm')
    sums = hist.ProjectionX()
    for xbin in range(1, hist.GetNbinsX() + 1):
        the_sum = sums.GetBinContent(xbin)
        print 'sum', the_sum
        if the_sum == 0:
            continue
        for ybin in range(1, hist.GetNbinsY() + 1):
            value = hist.GetBinContent(xbin, ybin) / the_sum
            print value
            hist_norm.SetBinContent(xbin, ybin, value)
    return hist_norm
        
    
if __name__ == '__main__':
    # DEAL WITH NEG VALUES
    
    csvmap = CSVMap()
    nbins = 121 * 10
    csvmap.build_map('qcd.root', 10, 0, 100, nbins, -11, 1.1)
    
