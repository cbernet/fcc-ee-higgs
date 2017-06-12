from ROOT import RooRealVar, RooPolynomial, RooDataSet, RooDataHist, RooHistPdf, RooGaussian, RooArgSet, RooAddPdf, RooArgList, RooFit
from ROOT import TCanvas

import math

x = RooRealVar("x","x", 50, 150);
x.setBins(100)

nsig = 1000
ysig = 1
ybgd = 8 * ysig
ndata = nsig * (1 + ybgd / ysig) 

######### underlying model 

mean = RooRealVar("mean","mean", 125, 100, 150);
sigma = RooRealVar("sigma","sigma", 2, 0, 10);

sig = RooGaussian("sig", "sig", x, mean, sigma)
bgd = RooPolynomial("bgd", "bgd", x)               

c1 = TCanvas()

pframe = x.frame() 
sig.plotOn(pframe)
bgd.plotOn(pframe)
pframe.Draw()

vysig = RooRealVar("nsig", 'nsig', ysig, 0, 100000)
vybgd = RooRealVar("nbgd", 'nbgd', ybgd, 0, 100000)
model = RooAddPdf("model", "model", RooArgList(sig, bgd),
                  RooArgList(vysig, vybgd))
#model = RooAddPdf("model", "model", RooArgList(sig),
#                  RooArgList(vysig))

c2 = TCanvas()

mframe = x.frame()
model.plotOn(mframe)
mframe.Draw()


######### data generation, parametrized

data = model.generate(RooArgSet(x), ndata)

######### fit, parametrized

result = model.fitTo(data, RooFit.Extended(), RooFit.Save())

cf_p = TCanvas('cf_p', 'fit, parametrized')

cf_p_frame = x.frame()
data.plotOn(cf_p_frame)
model.plotOn(cf_p_frame)
cf_p_frame.Draw()


######### model definition, template  

nsig_tpl = 10000
nbgd_tpl = 1000000

exp_sig_data = sig.generate(RooArgSet(x), nsig_tpl)
exp_sig_hist = exp_sig_data.binnedClone()
tsig = RooHistPdf('tsig', 'tsig', RooArgSet(x), exp_sig_hist)

exp_bgd_data = bgd.generate(RooArgSet(x), nbgd_tpl)
exp_bgd_hist = exp_bgd_data.binnedClone()
tbgd = RooHistPdf('tbgd', 'tbgd', RooArgSet(x), exp_bgd_hist)

# modelsig = RooAddPdf("modelsig", "modelsig", RooArgList(tsig), RooArgList(vysig))
# tmodel = RooAddPdf("tmodel", "tmodel", RooArgList(tsig), RooArgList(vysig))
tmodel = RooAddPdf("tmodel", "tmodel", RooArgList(tsig, tbgd),
                   RooArgList(vysig, vybgd))

######### data generation, template 

tdata = tmodel.generate(RooArgSet(x), ndata)

######### fit, template

tresult = tmodel.fitTo(tdata, RooFit.Extended(), RooFit.Save())

c4 = TCanvas()

oframe = x.frame()
tdata.plotOn(oframe)
tmodel.plotOn(oframe)
oframe.Draw()

######### final printing and output

print 'Parametrized:'
print '-' * 70
result.Print()

print
print '-' * 70
print 'Template:'
tresult.Print()
