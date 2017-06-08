from ROOT import RooRealVar, RooPolynomial, RooDataSet, RooDataHist, RooHistPdf, RooGaussian, RooArgSet, RooAddPdf, RooArgList, RooFit
from ROOT import TCanvas

x = RooRealVar("x","x", 50, 150);
x.setBins(100)
mean = RooRealVar("mean","mean", 125, 100, 150);
sigma = RooRealVar("sigma","sigma", 2, 0, 10);
sig = RooGaussian("sig", "sig", x, mean, sigma)

bgd = RooPolynomial("bgd", "bgd", x)               

pframe = x.frame() 
sig.plotOn(pframe)
bgd.plotOn(pframe)
pframe.Draw()

ysig = 1000
ybak = 8 * ysig
vysig = RooRealVar("nsig", 'nsig', ysig, 0, 10000)
vybak = RooRealVar("nbak", 'nbak', ybak, 0, 10000)
model = RooAddPdf("model", "model", RooArgList(sig, bgd),
                  RooArgList(vysig, vybak))

mframe = x.frame()
model.plotOn(mframe)
mframe.Draw()

nsig = 100
nbak = 10000
exp_sig_data = sig.generate(RooArgSet(x), nsig)
exp_sig_hist = exp_sig_data.binnedClone()
tsig = RooHistPdf('tsig', 'tsig', RooArgSet(x), exp_sig_hist)

dframe = x.frame()
exp_sig_data.plotOn(dframe)
tsig.plotOn(dframe)
dframe.Draw()

data = sig.generate(RooArgSet(x), nsig*10)
tresult = tsig.fitTo(data, RooFit.Extended())

oframe = x.frame()
data.plotOn(oframe)
tsig.plotOn(oframe)
oframe.Draw()
