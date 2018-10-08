
def flatten(hist):
    hist.Fit("pol0")
    func = hist.GetFunction("pol0")
    norm = func.GetParameter(0)
    new_hist = hist.Clone()
    for bin in range(1, new_hist.GetXaxis().GetNbins() + 1):
        new_hist.SetBinContent(bin, norm)
    return new_hist
        
        
