import random

def prob(pdf, mass):
    ibin = pdf.FindBin(mass)
    return pdf.GetBinContent(ibin)


def is_btagged(bmatch, wp):
    rnd = random.uniform(0, 1)
    if bmatch:
        return rnd < wp[0]
    else:
        return rnd < wp[1]

def prob_b(j1bmatch, j2bmatch, wp):
    b1 = is_btagged(j1bmatch, wp)
    b2 = is_btagged(j2bmatch, wp)
    if b1 and b2:
        return wp[0] ** 2
    elif not b1 and not b2:
        return wp[1] ** 2
    else:
        return 1 - wp[0] ** 2 - wp[1] ** 2

if __name__ == '__main__':
    

    import sys
    import time
    import copy
    from optparse import OptionParser
    from ROOT import TFile, TH1F

    from fcc_ee_higgs.plot.plotconfig_ZH_ll import b_wp

    parser = OptionParser()
    parser.add_option('-p', '--pdfs',
                      dest='pdfs',
                      action="store_true", default=False, 
                      help="extract the mass pdfs")
    
    options, args = parser.parse_args(sys.argv)    
        
    ifile = TFile(args[1])
    itree = ifile.Get('events')
 
    nbins, xmin, xmax = 50, 0, 200
    if options.pdfs:
        pdf_zed = TH1F("pdf_zed", "", nbins, xmin, xmax)
        trucut = "higgs_1_bfrac>0.2 && higgs_2_bfrac>0.2"
        itree.Project("pdf_zed", "zed_m",
                      trucut)
        pdf_zed.Scale(1/pdf_zed.Integral())
        pdf_higgs = TH1F("pdf_higgs", "", nbins, xmin, xmax)
        itree.Project("pdf_higgs", "higgs_m",
                        trucut)
        pdf_higgs.Draw()
        pdf_higgs.Scale(1/pdf_higgs.Integral())
        pdf_zed.Draw('same')
        
    higgs_mass = TH1F("higgs_mass", "higgs_mass", nbins, xmin, xmax)

    bestmass = -2
    maxlh = 0
    for hypo in itree:
        if hypo.hid == 0 and bestmass > -1:
            higgs_mass.Fill(bestmass)
            maxlh = 0
            # print '=' * 70
        # print hypo.hid
        # print hypo.higgs_m, hypo.zed_m
        p_h = prob(pdf_higgs, hypo.higgs_m)
        p_z = prob(pdf_zed, hypo.zed_m)
        p_b = prob_b(hypo.higgs_1_bmatch, hypo.higgs_2_bmatch, b_wp)
        lh = p_h * p_z * p_b
        # print p_h, p_z, lh
        if bestmass < 0 or lh > maxlh:
            bestmass = hypo.higgs_m
            maxlh = lh
            
    higgs_mass.Draw()
