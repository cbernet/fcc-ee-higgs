
import ROOT

from fcc_ee_higgs.plot.plotconfig_ilc_ZH_ll import ZH, WW, ZZ, cuts

ntuple_sig = ZH.tree
ntuple_bgd = ZZ.tree

if 'cut_mvaww' in cuts:
    del cuts['cut_mvaww']   
cuts['massrange'] = 'recoil_m>110'
cut = str(cuts)

# keeps objects otherwise removed by garbage collected in a list
gcSaver = []

# create a new TCanvas
gcSaver.append(ROOT.TCanvas())

ROOT.TMVA.Tools.Instance()

# note that it seems to be mandatory to have an
# output file, just passing None to TMVA::Factory(..)
# does not work. Make sure you don't overwrite an
# existing file.
fout = ROOT.TFile("test.root","RECREATE")

factory = ROOT.TMVA.Factory("TMVAClassification", fout,
                            ":".join([
                                "!V",
                                "!Silent",
                                "Color",
                                "DrawProgressBar",
                                "Transformations=I;D;P;G,D",
                                "AnalysisType=Classification"]
                                     ))

dataloader = ROOT.TMVA.DataLoader("dataset")

variables = ['zeds_m',
             'zeds_theta',
             'zeds_1_theta', 'zeds_2_theta',
             'zeds_acol']
for variable in variables:
    dataloader.AddVariable(variable, 'F')

signalWeight = 1.
backgroundWeight = 1.
dataloader.AddSignalTree    ( ntuple_sig,     signalWeight     )
dataloader.AddBackgroundTree( ntuple_bgd, backgroundWeight )

mycutSig = ROOT.TCut(cut)
mycutBkg = ROOT.TCut(cut)
dataloader.PrepareTrainingAndTestTree( mycutSig, mycutBkg,
                                       "nTrain_Signal=0:nTrain_Background=0:SplitMode=Random:NormMode=NumEvents:!V" )

factory.BookMethod( dataloader, ROOT.TMVA.Types.kBDT, "BDTG",
                    "!H:!V:NTrees=1000:MinNodeSize=1.5%:BoostType=Grad:Shrinkage=0.10:UseBaggedBoost:BaggedSampleFraction=0.5:nCuts=20:MaxDepth=2" )        


# Train MVAs
factory.TrainAllMethods()

# Test MVAs
factory.TestAllMethods()

# Evaluate MVAs
factory.EvaluateAllMethods()    

fout.Close()
ROOT.TMVA.TMVAGui(fout.GetName())

##
##factory.AddSignalTree(ntuple)
##factory.AddBackgroundTree(ntuple)
##
### cuts defining the signal and background sample
##sigCut = ROOT.TCut("signal > 0.5")
##bgCut = ROOT.TCut("signal <= 0.5")
##
##factory.PrepareTrainingAndTestTree(sigCut,   # signal events
##                                   bgCut,    # background events
##                                   ":".join([
##                                       "nTrain_Signal=0",
##                                        "nTrain_Background=0",
##                                        "SplitMode=Random",
##                                        "NormMode=NumEvents",
##                                        "!V"
##                                   ]))
