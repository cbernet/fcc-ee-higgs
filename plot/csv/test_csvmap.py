import unittest
from fcc_ee_higgs.plot.csv.csvmap import CSVMap

def readmap():
    csvmap = CSVMap()
    csvmap.read('csvmaps.root')
    return csvmap

class TestCSVMap(unittest.TestCase):
    
    def test_1_fill_map(self):
        csvmap = CSVMap()
        nbins = 121 * 10
        csvmap.build_map('qcd.root', 7, 30, 100, nbins, -11, 1.1)
        
    def test_2_read_map(self):
        csvmap = readmap()
        self.assertTrue(csvmap.histmap_b)
        self.assertTrue(csvmap.histmap_other)
        self.assertEqual(csvmap.histmap_b.GetNbinsX(),
                         len(csvmap.histmaps1d_b))
        
    def test_3_rightmap(self):
        csvmap = readmap()
        pdf = csvmap.pdf(30, True)
        self.assertEqual(pdf, csvmap.histmaps1d_b[1])
        pdf = csvmap.pdf(45, True)
        self.assertEqual(pdf, csvmap.histmaps1d_b[2])
        pdf = csvmap.pdf(55, False)
        self.assertEqual(pdf, csvmap.histmaps1d_other[3])
        
    def test_4_ptrange(self):
        csvmap = readmap()
        pdf = csvmap.pdf(105, True)
        self.assertEqual(pdf, csvmap.histmaps1d_b[7])
        self.assertEqual(csvmap.value(25, True), -15)
        
if __name__ == '__main__':
    unittest.main()
