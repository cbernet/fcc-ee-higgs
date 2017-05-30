from ROOT import RooRealVar, RooDataSet, RooDataHist, RooHistPdf, RooGaussian, RooArgSet, RooAddPdf, RooArgList, RooFit
from ROOT import TCanvas

x = RooRealVar("x","x",-10,10);
x.setBins(50)
mean = RooRealVar("mean","mean",2,-10,10);
sigma = RooRealVar("sigma","sigma",1,-10,10);

sig = RooGaussian("sig", "sig", x, mean, sigma)


mean2 = RooRealVar("mean2","mean2",-5,-10,10);
sigma2 = RooRealVar("sigma2","sigma2",5,-10,10);
bgd = RooGaussian("bgd", "bgd", x, mean2, sigma2)

nsig = RooRealVar("nsig", 'nsig', 50, 0, 10000)
nbak = RooRealVar("nbak", 'nbak', 200, 0, 10000)
model = RooAddPdf("model", "model", RooArgList(sig, bgd), RooArgList(nsig, nbak))

# histogram templates
sigdata = sig.generate(RooArgSet(x), 1000)
sighist = sigdata.binnedClone()
tsig = RooHistPdf('tsig', 'tsig', RooArgSet(x), sighist)

bgddata = bgd.generate(RooArgSet(x), 10000)
bgdhist = bgddata.binnedClone()
tbgd = RooHistPdf('tbgd', 'tbgd', RooArgSet(x), bgdhist)

tmodel = RooAddPdf("tmodel", "tmodel", RooArgList(tsig, tbgd), RooArgList(nsig, nbak))

pframe = x.frame() 
sig.plotOn(pframe)
bgd.plotOn(pframe)
model.plotOn(pframe)

tframe = x.frame() 
tsig.plotOn(tframe)
tbgd.plotOn(tframe)



data = model.generate(RooArgSet(x), 1000)

result = model.fitTo(data, RooFit.Extended())
tresult = tmodel.fitTo(data, RooFit.Extended())

c1 = TCanvas()
pframe.Draw()

c3 = TCanvas()
tframe.Draw()

c2 = TCanvas()
dframe = x.frame()
data.plotOn(dframe)
model.plotOn(dframe)
model.plotOn(dframe, RooFit.Components("bgd"), RooFit.LineColor(3))
model.plotOn(dframe, RooFit.Components("sig"), RooFit.LineColor(2))
dframe.Draw()

c4 = TCanvas()
tdframe = x.frame()
data.plotOn(tdframe)
tmodel.plotOn(tdframe)
tmodel.plotOn(tdframe, RooFit.Components("tbgd"), RooFit.LineColor(3))
tmodel.plotOn(tdframe, RooFit.Components("tsig"), RooFit.LineColor(2))
tdframe.Draw()
